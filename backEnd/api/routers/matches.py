"""
Matches/Fixtures endpoints.
Provides access to live matches, upcoming fixtures, and match details.
"""
from typing import List, Optional
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query, HTTPException, status

from backEnd.controllers.football_controller import FootballController
from backEnd.api.dependencies import get_football_controller
from backEnd.schemas.analytics import (
    FixtureResponse,
    LiveFixturesResponse,
    MatchStatisticsResponse,
    MatchEventsResponse,
    LineupsResponse,
    HeadToHeadResponse
)

router = APIRouter()


@router.get("/live", response_model=dict)
async def get_live_matches(
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get all currently live matches.
    
    Returns:
        List of live fixtures with scores and status
    """
    try:
        fixtures = await controller.get_live_fixtures()
        return {
            "count": len(fixtures),
            "fixtures": fixtures
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching live matches: {str(e)}"
        )


@router.get("/today", response_model=dict)
async def get_today_matches(
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get all matches for today.
    
    Returns:
        List of today's fixtures
    """
    try:
        fixtures = await controller.get_fixtures_by_date(date.today())
        return {
            "date": date.today().isoformat(),
            "count": len(fixtures),
            "fixtures": fixtures
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching today's matches: {str(e)}"
        )


@router.get("/date/{target_date}", response_model=dict)
async def get_matches_by_date(
    target_date: date,
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get matches for a specific date.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        List of fixtures for the specified date
    """
    try:
        fixtures = await controller.get_fixtures_by_date(target_date)
        return {
            "date": target_date.isoformat(),
            "count": len(fixtures),
            "fixtures": fixtures
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching matches for date: {str(e)}"
        )


@router.get("/league/{league_id}", response_model=dict)
async def get_league_fixtures(
    league_id: int,
    season: int = Query(..., description="Season year (e.g., 2023)"),
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    round_name: Optional[str] = Query(None, description="Specific round"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get fixtures for a specific league and season.
    
    Args:
        league_id: League ID
        season: Season year
        from_date: Optional start date filter
        to_date: Optional end date filter
        round_name: Optional round filter
        
    Returns:
        List of league fixtures
    """
    try:
        fixtures = await controller.get_fixtures_by_league(
            league_id=league_id,
            season=season,
            from_date=from_date,
            to_date=to_date,
            round_name=round_name
        )
        return {
            "league_id": league_id,
            "season": season,
            "count": len(fixtures),
            "fixtures": fixtures
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching league fixtures: {str(e)}"
        )


@router.get("/team/{team_id}", response_model=dict)
async def get_team_fixtures(
    team_id: int,
    season: Optional[int] = Query(None, description="Season year"),
    last: Optional[int] = Query(None, description="Last N fixtures"),
    next: Optional[int] = Query(None, description="Next N fixtures"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get fixtures for a specific team.
    
    Args:
        team_id: Team ID
        season: Optional season filter
        last: Get last N fixtures
        next: Get next N fixtures
        
    Returns:
        List of team fixtures
    """
    try:
        fixtures = await controller.get_team_fixtures(
            team_id=team_id,
            season=season,
            last=last,
            next=next
        )
        return {
            "team_id": team_id,
            "count": len(fixtures),
            "fixtures": fixtures
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching team fixtures: {str(e)}"
        )


@router.get("/{fixture_id}", response_model=dict)
async def get_fixture_details(
    fixture_id: int,
    include_statistics: bool = Query(False, description="Include match statistics"),
    include_events: bool = Query(False, description="Include match events"),
    include_lineups: bool = Query(False, description="Include team lineups"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get detailed information for a specific fixture.
    
    Args:
        fixture_id: Fixture ID
        include_statistics: Include match statistics
        include_events: Include match events (goals, cards, subs)
        include_lineups: Include team lineups
        
    Returns:
        Comprehensive fixture data
    """
    try:
        fixture_data = await controller.get_fixture_details(
            fixture_id=fixture_id,
            include_statistics=include_statistics,
            include_events=include_events,
            include_lineups=include_lineups
        )
        return fixture_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching fixture details: {str(e)}"
        )


@router.get("/{fixture_id}/statistics", response_model=dict)
async def get_fixture_statistics(
    fixture_id: int,
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get match statistics for a fixture.
    
    Args:
        fixture_id: Fixture ID
        
    Returns:
        Match statistics (shots, possession, passes, etc.)
    """
    try:
        fixture_data = await controller.get_fixture_details(
            fixture_id=fixture_id,
            include_statistics=True
        )
        return {
            "fixture_id": fixture_id,
            "statistics": fixture_data.get("statistics", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching fixture statistics: {str(e)}"
        )


@router.get("/{fixture_id}/events", response_model=dict)
async def get_fixture_events(
    fixture_id: int,
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get match events (goals, cards, substitutions) for a fixture.
    
    Args:
        fixture_id: Fixture ID
        
    Returns:
        Match events timeline
    """
    try:
        fixture_data = await controller.get_fixture_details(
            fixture_id=fixture_id,
            include_events=True
        )
        return {
            "fixture_id": fixture_id,
            "events": fixture_data.get("events", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching fixture events: {str(e)}"
        )


@router.get("/{fixture_id}/lineups", response_model=dict)
async def get_fixture_lineups(
    fixture_id: int,
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get team lineups for a fixture.
    
    Args:
        fixture_id: Fixture ID
        
    Returns:
        Team lineups with formations
    """
    try:
        fixture_data = await controller.get_fixture_details(
            fixture_id=fixture_id,
            include_lineups=True
        )
        return {
            "fixture_id": fixture_id,
            "lineups": fixture_data.get("lineups", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching fixture lineups: {str(e)}"
        )


@router.get("/h2h/{team1_id}/{team2_id}", response_model=dict)
async def get_head_to_head(
    team1_id: int,
    team2_id: int,
    last: Optional[int] = Query(10, description="Number of last matches"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get head-to-head matches between two teams.
    
    Args:
        team1_id: First team ID
        team2_id: Second team ID
        last: Number of last matches to retrieve
        
    Returns:
        Head-to-head fixture history
    """
    try:
        fixtures = await controller.get_head_to_head(
            team1_id=team1_id,
            team2_id=team2_id,
            last=last
        )
        return {
            "team1_id": team1_id,
            "team2_id": team2_id,
            "total_matches": len(fixtures),
            "fixtures": fixtures
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching head-to-head: {str(e)}"
        )
