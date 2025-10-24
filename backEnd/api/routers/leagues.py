"""League endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_league_service
from services.service import LeagueService
from schemas.league import LeagueResponse, LeagueCreate, LeagueUpdate

router = APIRouter()


@router.get("/", response_model=List[LeagueResponse])
def list_leagues(
    limit: int = 100,
    offset: int = 0,
    service: LeagueService = Depends(get_league_service)
):
    """Get all leagues with pagination."""
    return service.list(limit=limit, offset=offset)


@router.get("/{league_id}", response_model=LeagueResponse)
def get_league(
    league_id: int,
    service: LeagueService = Depends(get_league_service)
):
    """Get a specific league by ID."""
    league = service.get(league_id)
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"League with ID {league_id} not found"
        )
    return league


@router.post("/", response_model=LeagueResponse, status_code=status.HTTP_201_CREATED)
def create_league(
    league_data: LeagueCreate,
    service: LeagueService = Depends(get_league_service)
):
    """Create a new league."""
    return service.create(league_data)


@router.put("/{league_id}", response_model=LeagueResponse)
def update_league(
    league_id: int,
    league_data: LeagueUpdate,
    service: LeagueService = Depends(get_league_service)
):
    """Update an existing league."""
    league = service.update(league_id, league_data)
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"League with ID {league_id} not found"
        )
    return league


@router.delete("/{league_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_league(
    league_id: int,
    service: LeagueService = Depends(get_league_service)
):
    """Delete a league."""
    league = service.delete(league_id)
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"League with ID {league_id} not found"
        )
    return None


@router.get("/{league_id}/seasons")
def get_league_seasons(
    league_id: int,
    service: LeagueService = Depends(get_league_service)
):
    """Get all seasons for a specific league."""
    return service.get_seasons(league_id)
