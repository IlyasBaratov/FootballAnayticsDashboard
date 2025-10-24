"""Team endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from backEnd.api.dependencies import get_team_service
from backEnd.services.service import TeamService
from backEnd.schemas.team import TeamResponse, TeamCreate, TeamUpdate

router = APIRouter()


@router.get("/", response_model=List[TeamResponse])
def list_teams(
    limit: int = 100,
    offset: int = 0,
    service: TeamService = Depends(get_team_service)
):
    """Get all teams with pagination."""
    return service.list(limit=limit, offset=offset)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    service: TeamService = Depends(get_team_service)
):
    """Get a specific team by ID."""
    team = service.get(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    return team


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: TeamCreate,
    service: TeamService = Depends(get_team_service)
):
    """Create a new team."""
    return service.create(team_data)


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_data: TeamUpdate,
    service: TeamService = Depends(get_team_service)
):
    """Update an existing team."""
    team = service.update(team_id, team_data)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    service: TeamService = Depends(get_team_service)
):
    """Delete a team."""
    team = service.delete(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    return None


@router.get("/{team_id}/fixtures")
def get_team_fixtures(
    team_id: int,
    service: TeamService = Depends(get_team_service)
):
    """Get all fixtures for a specific team."""
    return service.get_fixtures(team_id)
