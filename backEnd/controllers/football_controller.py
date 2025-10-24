"""
Football controller for managing API-Football data integration.
Handles fetching, caching, and syncing data from external API to database.
"""
import logging
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from services.api_football_client import APIFootballClient, get_api_football_client
from models.model import (
    League, Season, Team, Venue, Fixture, Player, 
    Standing, Coach, PlayerTeamSeason
)
from repository.rep import Repository

logger = logging.getLogger(__name__)


class FootballController:
    """
    Controller for football data operations.
    
    Integrates with API-Football to fetch and sync data to local database.
    """
    
    def __init__(
        self, 
        db: Session,
        api_client: Optional[APIFootballClient] = None
    ):
        """
        Initialize controller.
        
        Args:
            db: Database session
            api_client: API-Football client (uses singleton if not provided)
        """
        self.db = db
        self.api_client = api_client or get_api_football_client()
        
        # Initialize repositories
        self.league_repo = Repository(League)
        self.season_repo = Repository(Season)
        self.team_repo = Repository(Team)
        self.venue_repo = Repository(Venue)
        self.fixture_repo = Repository(Fixture)
        self.player_repo = Repository(Player)
        self.standing_repo = Repository(Standing)
    
    # ============ LEAGUES ============
    
    async def sync_league(self, league_id: int, season: Optional[int] = None) -> League:
        """
        Fetch league from API and sync to database.
        
        Args:
            league_id: API-Football league ID
            season: Optional season year
            
        Returns:
            League model instance
        """
        try:
            # Fetch from API
            response = await self.api_client.get_leagues(
                league_id=league_id,
                season=season
            )
            
            if not response.get("response"):
                raise ValueError(f"League {league_id} not found in API")
            
            league_data = response["response"][0]
            league_info = league_data["league"]
            country_info = league_data["country"]
            
            # Check if league exists
            existing_league = self.league_repo.get(self.db, league_id)
            
            league_dict = {
                "id": league_info["id"],
                "name": league_info["name"],
                "type": league_info["type"],
                "logo": league_info.get("logo"),
                "country": country_info.get("name"),
                "country_code": country_info.get("code"),
                "flag": country_info.get("flag")
            }
            
            if existing_league:
                # Update existing
                for key, value in league_dict.items():
                    setattr(existing_league, key, value)
                existing_league.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(existing_league)
                logger.info(f"Updated league: {existing_league.name}")
                return existing_league
            else:
                # Create new
                new_league = League(**league_dict)
                self.db.add(new_league)
                self.db.commit()
                self.db.refresh(new_league)
                logger.info(f"Created league: {new_league.name}")
                return new_league
                
        except Exception as e:
            logger.error(f"Error syncing league {league_id}: {e}")
            self.db.rollback()
            raise
    
    async def get_available_leagues(
        self, 
        country: Optional[str] = None,
        current: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get available leagues from API.
        
        Args:
            country: Filter by country
            current: Only current leagues
            
        Returns:
            List of league data from API
        """
        try:
            response = await self.api_client.get_leagues(
                country=country,
                current=current
            )
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching leagues: {e}")
            raise
    
    # ============ TEAMS ============
    
    async def sync_team(
        self, 
        team_id: int,
        league_id: Optional[int] = None,
        season: Optional[int] = None
    ) -> Team:
        """
        Fetch team from API and sync to database.
        
        Args:
            team_id: API-Football team ID
            league_id: Optional league ID for context
            season: Optional season year
            
        Returns:
            Team model instance
        """
        try:
            response = await self.api_client.get_teams(
                team_id=team_id,
                league=league_id,
                season=season
            )
            
            if not response.get("response"):
                raise ValueError(f"Team {team_id} not found in API")
            
            team_data = response["response"][0]
            team_info = team_data["team"]
            venue_info = team_data.get("venue")
            
            # Sync venue if present
            venue = None
            if venue_info and venue_info.get("id"):
                venue = await self.sync_venue(venue_info)
            
            # Check if team exists
            existing_team = self.team_repo.get(self.db, team_id)
            
            team_dict = {
                "id": team_info["id"],
                "name": team_info["name"],
                "short_code": team_info.get("code"),
                "country": team_info.get("country"),
                "founded": team_info.get("founded"),
                "national": team_info.get("national", False),
                "logo": team_info.get("logo"),
                "venue_id": venue.id if venue else None
            }
            
            if existing_team:
                for key, value in team_dict.items():
                    setattr(existing_team, key, value)
                existing_team.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(existing_team)
                logger.info(f"Updated team: {existing_team.name}")
                return existing_team
            else:
                new_team = Team(**team_dict)
                self.db.add(new_team)
                self.db.commit()
                self.db.refresh(new_team)
                logger.info(f"Created team: {new_team.name}")
                return new_team
                
        except Exception as e:
            logger.error(f"Error syncing team {team_id}: {e}")
            self.db.rollback()
            raise
    
    async def sync_venue(self, venue_data: Dict[str, Any]) -> Optional[Venue]:
        """
        Sync venue to database.
        
        Args:
            venue_data: Venue data from API
            
        Returns:
            Venue model instance or None
        """
        try:
            if not venue_data or not venue_data.get("id"):
                return None
            
            venue_id = venue_data["id"]
            existing_venue = self.venue_repo.get(self.db, venue_id)
            
            venue_dict = {
                "id": venue_id,
                "name": venue_data.get("name"),
                "city": venue_data.get("city"),
                "capacity": venue_data.get("capacity"),
                "surface": venue_data.get("surface"),
                "address": venue_data.get("address")
            }
            
            if existing_venue:
                for key, value in venue_dict.items():
                    setattr(existing_venue, key, value)
                existing_venue.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(existing_venue)
                return existing_venue
            else:
                new_venue = Venue(**venue_dict)
                self.db.add(new_venue)
                self.db.commit()
                self.db.refresh(new_venue)
                return new_venue
                
        except Exception as e:
            logger.error(f"Error syncing venue: {e}")
            self.db.rollback()
            return None
    
    async def get_team_statistics(
        self,
        team_id: int,
        league_id: int,
        season: int
    ) -> Dict[str, Any]:
        """
        Get team statistics from API.
        
        Args:
            team_id: Team ID
            league_id: League ID
            season: Season year
            
        Returns:
            Team statistics data
        """
        try:
            response = await self.api_client.get_team_statistics(
                team_id=team_id,
                league=league_id,
                season=season
            )
            return response.get("response", {})
        except Exception as e:
            logger.error(f"Error fetching team statistics: {e}")
            raise
    
    # ============ FIXTURES (MATCHES) ============
    
    async def get_live_fixtures(self) -> List[Dict[str, Any]]:
        """
        Get all live fixtures from API.
        
        Returns:
            List of live fixture data
        """
        try:
            response = await self.api_client.get_live_fixtures()
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching live fixtures: {e}")
            raise
    
    async def get_fixtures_by_date(
        self,
        target_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """
        Get fixtures for a specific date.
        
        Args:
            target_date: Date to fetch (defaults to today)
            
        Returns:
            List of fixture data
        """
        try:
            if target_date is None:
                target_date = date.today()
            
            date_str = target_date.strftime("%Y-%m-%d")
            response = await self.api_client.get_fixtures_by_date(date_str)
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching fixtures by date: {e}")
            raise
    
    async def get_fixtures_by_league(
        self,
        league_id: int,
        season: int,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        round_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get fixtures for a league and season.
        
        Args:
            league_id: League ID
            season: Season year
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            round_name: Specific round
            
        Returns:
            List of fixture data
        """
        try:
            response = await self.api_client.get_fixtures(
                league=league_id,
                season=season,
                from_date=from_date,
                to_date=to_date,
                round=round_name
            )
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching league fixtures: {e}")
            raise
    
    async def get_fixture_details(
        self,
        fixture_id: int,
        include_statistics: bool = False,
        include_events: bool = False,
        include_lineups: bool = False
    ) -> Dict[str, Any]:
        """
        Get detailed fixture information.
        
        Args:
            fixture_id: Fixture ID
            include_statistics: Include match statistics
            include_events: Include match events
            include_lineups: Include team lineups
            
        Returns:
            Comprehensive fixture data
        """
        try:
            # Get basic fixture data
            fixture_response = await self.api_client.get_fixtures(fixture_id=fixture_id)
            
            if not fixture_response.get("response"):
                raise ValueError(f"Fixture {fixture_id} not found")
            
            fixture_data = fixture_response["response"][0]
            
            # Optionally fetch additional data
            if include_statistics:
                stats_response = await self.api_client.get_fixture_statistics(fixture_id)
                fixture_data["statistics"] = stats_response.get("response", [])
            
            if include_events:
                events_response = await self.api_client.get_fixture_events(fixture_id)
                fixture_data["events"] = events_response.get("response", [])
            
            if include_lineups:
                lineups_response = await self.api_client.get_fixture_lineups(fixture_id)
                fixture_data["lineups"] = lineups_response.get("response", [])
            
            return fixture_data
            
        except Exception as e:
            logger.error(f"Error fetching fixture details: {e}")
            raise
    
    async def get_team_fixtures(
        self,
        team_id: int,
        season: Optional[int] = None,
        last: Optional[int] = None,
        next: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get fixtures for a team.
        
        Args:
            team_id: Team ID
            season: Optional season year
            last: Get last N fixtures
            next: Get next N fixtures
            
        Returns:
            List of fixture data
        """
        try:
            response = await self.api_client.get_fixtures(
                team=team_id,
                season=season,
                last=last,
                next=next
            )
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching team fixtures: {e}")
            raise
    
    # ============ STANDINGS ============
    
    async def get_standings(
        self,
        league_id: int,
        season: int,
        team_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get league standings from API.
        
        Args:
            league_id: League ID
            season: Season year
            team_id: Optional specific team
            
        Returns:
            Standings data
        """
        try:
            response = await self.api_client.get_standings(
                league=league_id,
                season=season,
                team=team_id
            )
            
            if response.get("response"):
                return response["response"][0].get("league", {}).get("standings", [])
            return []
            
        except Exception as e:
            logger.error(f"Error fetching standings: {e}")
            raise
    
    # ============ PLAYERS ============
    
    async def get_top_scorers(
        self,
        league_id: int,
        season: int
    ) -> List[Dict[str, Any]]:
        """
        Get top scorers for a league and season.
        
        Args:
            league_id: League ID
            season: Season year
            
        Returns:
            List of top scorer data
        """
        try:
            response = await self.api_client.get_top_scorers(
                league=league_id,
                season=season
            )
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching top scorers: {e}")
            raise
    
    async def get_top_assists(
        self,
        league_id: int,
        season: int
    ) -> List[Dict[str, Any]]:
        """
        Get top assists for a league and season.
        
        Args:
            league_id: League ID
            season: Season year
            
        Returns:
            List of top assist data
        """
        try:
            response = await self.api_client.get_top_assists(
                league=league_id,
                season=season
            )
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching top assists: {e}")
            raise
    
    async def search_players(
        self,
        search_term: str,
        league_id: Optional[int] = None,
        season: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for players by name.
        
        Args:
            search_term: Player name to search
            league_id: Optional league filter
            season: Optional season filter
            
        Returns:
            List of player data
        """
        try:
            response = await self.api_client.get_players(
                search=search_term,
                league=league_id,
                season=season
            )
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error searching players: {e}")
            raise
    
    # ============ PREDICTIONS & HEAD TO HEAD ============
    
    async def get_predictions(self, fixture_id: int) -> Dict[str, Any]:
        """
        Get predictions for a fixture.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            Prediction data
        """
        try:
            response = await self.api_client.get_predictions(fixture_id)
            
            if response.get("response"):
                return response["response"][0]
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching predictions: {e}")
            raise
    
    async def get_head_to_head(
        self,
        team1_id: int,
        team2_id: int,
        last: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get head to head matches between two teams.
        
        Args:
            team1_id: First team ID
            team2_id: Second team ID
            last: Number of last matches
            
        Returns:
            List of h2h fixture data
        """
        try:
            h2h_string = f"{team1_id}-{team2_id}"
            response = await self.api_client.get_head_to_head(
                h2h=h2h_string,
                last=last
            )
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching head to head: {e}")
            raise
    
    # ============ UTILITY METHODS ============
    
    async def get_countries(self) -> List[Dict[str, Any]]:
        """Get all available countries from API."""
        try:
            response = await self.api_client.get_countries()
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching countries: {e}")
            raise
    
    async def get_available_seasons(self) -> List[int]:
        """Get all available seasons from API."""
        try:
            response = await self.api_client.get_seasons()
            return response.get("response", [])
        except Exception as e:
            logger.error(f"Error fetching seasons: {e}")
            raise
