"""
Standings endpoints.
Provides access to league standings/tables.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status

from backEnd.controllers.football_controller import FootballController
from backEnd.api.dependencies import get_football_controller

router = APIRouter()


@router.get("/{league_id}", response_model=dict)
async def get_league_standings(
    league_id: int,
    season: int = Query(..., description="Season year (e.g., 2023)"),
    team_id: Optional[int] = Query(None, description="Filter by specific team"),
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get league standings/table for a specific season.
    
    Args:
        league_id: League ID
        season: Season year
        team_id: Optional team ID filter
        
    Returns:
        League standings with team positions, points, goals, etc.
    """
    try:
        standings = await controller.get_standings(
            league_id=league_id,
            season=season,
            team_id=team_id
        )
        
        if not standings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Standings not found for league {league_id} season {season}"
            )
        
        return {
            "league_id": league_id,
            "season": season,
            "standings": standings
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching standings: {str(e)}"
        )
