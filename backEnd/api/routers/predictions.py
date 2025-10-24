"""
Predictions endpoints.
Provides access to match predictions and forecasts.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from controllers.football_controller import FootballController
from api.dependencies import get_football_controller

router = APIRouter()


@router.get("/{fixture_id}", response_model=dict)
async def get_match_predictions(
    fixture_id: int,
    controller: FootballController = Depends(get_football_controller)
):
    """
    Get predictions for a specific fixture.
    
    Includes:
    - Win probability for each team
    - Goals predictions
    - Form comparison
    - Head-to-head history
    - Advice (home win, away win, draw)
    
    Args:
        fixture_id: Fixture ID
        
    Returns:
        Comprehensive prediction data
    """
    try:
        predictions = await controller.get_predictions(fixture_id)
        
        if not predictions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Predictions not available for fixture {fixture_id}"
            )
        
        return {
            "fixture_id": fixture_id,
            "predictions": predictions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching predictions: {str(e)}"
        )
