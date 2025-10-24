"""Player endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_player_service
from services.service import PlayerService
from schemas.player import PlayerResponse, PlayerCreate, PlayerUpdate

router = APIRouter()


@router.get("/", response_model=List[PlayerResponse])
def list_players(
    limit: int = 100,
    offset: int = 0,
    service: PlayerService = Depends(get_player_service)
):
    """Get all players with pagination."""
    return service.list(limit=limit, offset=offset)


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int,
    service: PlayerService = Depends(get_player_service)
):
    """Get a specific player by ID."""
    player = service.get(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return player


@router.post("/", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def create_player(
    player_data: PlayerCreate,
    service: PlayerService = Depends(get_player_service)
):
    """Create a new player."""
    return service.create(player_data)


@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(
    player_id: int,
    player_data: PlayerUpdate,
    service: PlayerService = Depends(get_player_service)
):
    """Update an existing player."""
    player = service.update(player_id, player_data)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return player


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(
    player_id: int,
    service: PlayerService = Depends(get_player_service)
):
    """Delete a player."""
    player = service.delete(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found"
        )
    return None


@router.get("/{player_id}/current-team")
def get_player_current_team(
    player_id: int,
    service: PlayerService = Depends(get_player_service)
):
    """Get the current team for a specific player."""
    team = service.get_current_team(player_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Current team not found for player with ID {player_id}"
        )
    return team
