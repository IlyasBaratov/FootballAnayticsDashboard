"""
Statistics endpoints.
Provides access to team statistics, top scorers, and analytics.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status

from controllers.football_controller import FootballController
from api.dependencies import get_football_controller

router = APIRouter()


@router.get("/team/{team_id}", response_model=dict)
async def get_team_statistics(
    team_id: int,
    league_id: int = Query(..., description="League ID"),
    season: int = Query(..., description="Season year"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get comprehensive team statistics for a season.
    
    Args:
        team_id: Team ID
        league_id: League ID
        season: Season year
        
    Returns:
        Team statistics including goals, wins, clean sheets, etc.
    """
    try:
        stats = await controller.get_team_statistics(
            team_id=team_id,
            league_id=league_id,
            season=season
        )
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Statistics not found for team {team_id}"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching team statistics: {str(e)}"
        )


@router.get("/top-scorers/{league_id}", response_model=dict)
async def get_top_scorers(
    league_id: int,
    season: int = Query(..., description="Season year"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get top scorers for a league and season.
    
    Args:
        league_id: League ID
        season: Season year
        
    Returns:
        List of top scorers with goals and statistics
    """
    try:
        scorers = await controller.get_top_scorers(
            league_id=league_id,
            season=season
        )
        
        return {
            "league_id": league_id,
            "season": season,
            "count": len(scorers),
            "top_scorers": scorers
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching top scorers: {str(e)}"
        )


@router.get("/top-assists/{league_id}", response_model=dict)
async def get_top_assists(
    league_id: int,
    season: int = Query(..., description="Season year"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get top assist providers for a league and season.
    
    Args:
        league_id: League ID
        season: Season year
        
    Returns:
        List of top assist providers with statistics
    """
    try:
        assists = await controller.get_top_assists(
            league_id=league_id,
            season=season
        )
        
        return {
            "league_id": league_id,
            "season": season,
            "count": len(assists),
            "top_assists": assists
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching top assists: {str(e)}"
        )


@router.get("/players/search", response_model=dict)
async def search_players(
    query: str = Query(..., min_length=2, description="Player name to search"),
    league_id: Optional[int] = Query(None, description="Filter by league"),
    season: Optional[int] = Query(None, description="Filter by season"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Search for players by name.
    
    Args:
        query: Player name search term (min 2 characters)
        league_id: Optional league filter
        season: Optional season filter
        
    Returns:
        List of matching players with statistics
    """
    try:
        players = await controller.search_players(
            search_term=query,
            league_id=league_id,
            season=season
        )
        
        return {
            "query": query,
            "count": len(players),
            "players": players
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching players: {str(e)}"
        )
