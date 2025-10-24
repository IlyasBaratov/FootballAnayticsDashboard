"""
API-Football external API client.
Handles all communication with the API-Football v3 API.
"""
import asyncio
import logging
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from functools import wraps

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# load .env variables
from dotenv import load_dotenv
load_dotenv()


class APIFootballError(Exception):
    """Base exception for API-Football errors."""
    pass


class APIFootballRateLimitError(APIFootballError):
    """Raised when API rate limit is exceeded."""
    pass


class APIFootballClient:
    """
    Client for API-Football v3 API.
    
    Features:
    - Automatic retry with exponential backoff
    - Rate limiting
    - Error handling
    - Request/response logging
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize API-Football client.
        
        Args:
            api_key: API-Football API key (defaults to settings)
            base_url: Base URL for API (defaults to settings)
        """
        self.api_key = api_key or settings.api_football_key
        self.base_url = base_url or settings.api_football_base_url
        self.timeout = settings.api_football_timeout
        
        if not self.api_key:
            raise ValueError("API_FOOTBALL_KEY must be set in environment variables or passed to client")
        
        self.headers = {
            "x-apisports-key": self.api_key,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        
        # Rate limiting
        self._request_times: List[float] = []
        self._rate_limit = settings.api_football_rate_limit
        
    async def _wait_for_rate_limit(self):
        """Implement rate limiting."""
        now = asyncio.get_event_loop().time()
        
        # Remove requests older than 1 minute
        self._request_times = [t for t in self._request_times if now - t < 60]
        
        if len(self._request_times) >= self._rate_limit:
            wait_time = 60 - (now - self._request_times[0])
            if wait_time > 0:
                logger.warning(f"Rate limit reached. Waiting {wait_time:.2f} seconds")
                await asyncio.sleep(wait_time)
                self._request_times = []
        
        self._request_times.append(now)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError))
    )
    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API-Football.
        
        Args:
            endpoint: API endpoint (e.g., "/leagues")
            params: Query parameters
            
        Returns:
            API response data
            
        Raises:
            APIFootballError: On API errors
            APIFootballRateLimitError: On rate limit errors
        """
        await self._wait_for_rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"API Request: GET {url} params={params}")
                
                response = await client.get(url, headers=self.headers, params=params)
                
                # Handle rate limiting
                if response.status_code == 429:
                    raise APIFootballRateLimitError("API rate limit exceeded")
                
                response.raise_for_status()
                data = response.json()
                
                # API-Football response structure
                if "errors" in data and data["errors"]:
                    raise APIFootballError(f"API Error: {data['errors']}")
                
                logger.info(f"API Response: {data.get('results', 0)} results")
                
                return data
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise APIFootballError(f"HTTP {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise APIFootballError(f"Request failed: {e}")
    
    # ============ LEAGUES ============
    
    async def get_leagues(
        self, 
        league_id: Optional[int] = None,
        name: Optional[str] = None,
        country: Optional[str] = None,
        season: Optional[int] = None,
        current: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get leagues/competitions.
        
        Args:
            league_id: Specific league ID
            name: League name
            country: Country name
            season: Season year (e.g., 2023)
            current: Only current leagues
            
        Returns:
            API response with leagues data
        """
        params = {}
        if league_id:
            params["id"] = league_id
        if name:
            params["name"] = name
        if country:
            params["country"] = country
        if season:
            params["season"] = season
        if current is not None:
            params["current"] = str(current).lower()
            
        return await self._make_request("/leagues", params)
    
    async def get_seasons(self) -> Dict[str, Any]:
        """Get all available seasons."""
        return await self._make_request("/leagues/seasons")
    
    # ============ TEAMS ============
    
    async def get_teams(
        self,
        team_id: Optional[int] = None,
        name: Optional[str] = None,
        league: Optional[int] = None,
        season: Optional[int] = None,
        country: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get teams.
        
        Args:
            team_id: Specific team ID
            name: Team name
            league: League ID
            season: Season year
            country: Country name
            
        Returns:
            API response with teams data
        """
        params = {}
        if team_id:
            params["id"] = team_id
        if name:
            params["name"] = name
        if league:
            params["league"] = league
        if season:
            params["season"] = season
        if country:
            params["country"] = country
            
        return await self._make_request("/teams", params)
    
    async def get_team_statistics(
        self,
        team_id: int,
        league: int,
        season: int
    ) -> Dict[str, Any]:
        """
        Get team statistics for a specific league and season.
        
        Args:
            team_id: Team ID
            league: League ID
            season: Season year
            
        Returns:
            API response with team statistics
        """
        params = {
            "team": team_id,
            "league": league,
            "season": season
        }
        return await self._make_request("/teams/statistics", params)
    
    # ============ FIXTURES (MATCHES) ============
    
    async def get_fixtures(
        self,
        fixture_id: Optional[int] = None,
        league: Optional[int] = None,
        season: Optional[int] = None,
        team: Optional[int] = None,
        date: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        round: Optional[str] = None,
        status: Optional[str] = None,
        live: Optional[str] = None,
        last: Optional[int] = None,
        next: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get fixtures/matches.
        
        Args:
            fixture_id: Specific fixture ID
            league: League ID
            season: Season year
            team: Team ID
            date: Specific date (YYYY-MM-DD)
            from_date: Start date
            to_date: End date
            round: Round name
            status: Match status (e.g., 'NS', 'LIVE', 'FT')
            live: Get live matches ('all' for all live matches)
            last: Last N fixtures
            next: Next N fixtures
            
        Returns:
            API response with fixtures data
        """
        params = {}
        if fixture_id:
            params["id"] = fixture_id
        if league:
            params["league"] = league
        if season:
            params["season"] = season
        if team:
            params["team"] = team
        if date:
            params["date"] = date
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if round:
            params["round"] = round
        if status:
            params["status"] = status
        if live:
            params["live"] = live
        if last:
            params["last"] = last
        if next:
            params["next"] = next
            
        return await self._make_request("/fixtures", params)
    
    async def get_fixtures_by_date(self, date: str) -> Dict[str, Any]:
        """
        Get fixtures for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            API response with fixtures
        """
        return await self.get_fixtures(date=date)
    
    async def get_live_fixtures(self) -> Dict[str, Any]:
        """Get all live fixtures."""
        return await self.get_fixtures(live="all")
    
    async def get_fixture_statistics(self, fixture_id: int) -> Dict[str, Any]:
        """
        Get statistics for a specific fixture.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            API response with fixture statistics
        """
        params = {"fixture": fixture_id}
        return await self._make_request("/fixtures/statistics", params)
    
    async def get_fixture_events(self, fixture_id: int) -> Dict[str, Any]:
        """
        Get events (goals, cards, substitutions) for a fixture.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            API response with fixture events
        """
        params = {"fixture": fixture_id}
        return await self._make_request("/fixtures/events", params)
    
    async def get_fixture_lineups(self, fixture_id: int) -> Dict[str, Any]:
        """
        Get lineups for a fixture.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            API response with lineups
        """
        params = {"fixture": fixture_id}
        return await self._make_request("/fixtures/lineups", params)
    
    async def get_fixture_player_statistics(self, fixture_id: int) -> Dict[str, Any]:
        """
        Get player statistics for a fixture.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            API response with player statistics
        """
        params = {"fixture": fixture_id}
        return await self._make_request("/fixtures/players", params)
    
    # ============ STANDINGS ============
    
    async def get_standings(
        self,
        league: int,
        season: int,
        team: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get league standings.
        
        Args:
            league: League ID
            season: Season year
            team: Specific team ID (optional)
            
        Returns:
            API response with standings
        """
        params = {
            "league": league,
            "season": season
        }
        if team:
            params["team"] = team
            
        return await self._make_request("/standings", params)
    
    # ============ PLAYERS ============
    
    async def get_players(
        self,
        player_id: Optional[int] = None,
        team: Optional[int] = None,
        league: Optional[int] = None,
        season: Optional[int] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get players.
        
        Args:
            player_id: Specific player ID
            team: Team ID
            league: League ID
            season: Season year
            search: Search by player name
            
        Returns:
            API response with players data
        """
        params = {}
        if player_id:
            params["id"] = player_id
        if team:
            params["team"] = team
        if league:
            params["league"] = league
        if season:
            params["season"] = season
        if search:
            params["search"] = search
            
        return await self._make_request("/players", params)
    
    async def get_player_seasons(self, player_id: int) -> Dict[str, Any]:
        """
        Get seasons available for a player.
        
        Args:
            player_id: Player ID
            
        Returns:
            API response with player seasons
        """
        params = {"player": player_id}
        return await self._make_request("/players/seasons", params)
    
    async def get_top_scorers(self, league: int, season: int) -> Dict[str, Any]:
        """
        Get top scorers for a league and season.
        
        Args:
            league: League ID
            season: Season year
            
        Returns:
            API response with top scorers
        """
        params = {
            "league": league,
            "season": season
        }
        return await self._make_request("/players/topscorers", params)
    
    async def get_top_assists(self, league: int, season: int) -> Dict[str, Any]:
        """
        Get top assists for a league and season.
        
        Args:
            league: League ID
            season: Season year
            
        Returns:
            API response with top assists
        """
        params = {
            "league": league,
            "season": season
        }
        return await self._make_request("/players/topassists", params)
    
    # ============ PREDICTIONS ============
    
    async def get_predictions(self, fixture_id: int) -> Dict[str, Any]:
        """
        Get predictions for a fixture.
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            API response with predictions
        """
        params = {"fixture": fixture_id}
        return await self._make_request("/predictions", params)
    
    # ============ HEAD TO HEAD ============
    
    async def get_head_to_head(
        self,
        h2h: str,
        date: Optional[str] = None,
        league: Optional[int] = None,
        season: Optional[int] = None,
        last: Optional[int] = None,
        next: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get head to head matches between two teams.
        
        Args:
            h2h: Team IDs separated by dash (e.g., "33-34")
            date: Specific date
            league: League ID
            season: Season year
            last: Last N matches
            next: Next N matches
            
        Returns:
            API response with head to head data
        """
        params = {"h2h": h2h}
        if date:
            params["date"] = date
        if league:
            params["league"] = league
        if season:
            params["season"] = season
        if last:
            params["last"] = last
        if next:
            params["next"] = next
            
        return await self._make_request("/fixtures/headtohead", params)
    
    # ============ COUNTRIES & TIMEZONES ============
    
    async def get_countries(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get available countries.
        
        Args:
            name: Country name filter
            
        Returns:
            API response with countries
        """
        params = {}
        if name:
            params["name"] = name
        return await self._make_request("/countries", params)
    
    async def get_timezones(self) -> Dict[str, Any]:
        """Get available timezones."""
        return await self._make_request("/timezone")


# Singleton instance
_client: Optional[APIFootballClient] = None


def get_api_football_client() -> APIFootballClient:
    """Get or create singleton API-Football client."""
    global _client
    if _client is None:
        _client = APIFootballClient()
    return _client
