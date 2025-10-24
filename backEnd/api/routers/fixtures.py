"""Fixture endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from backEnd.api.dependencies import get_fixture_service
from backEnd.services.service import FixtureService
from backEnd.schemas.fixture import FixtureResponse, FixtureCreate, FixtureUpdate, FixtureDetailResponse

router = APIRouter()


@router.get("/", response_model=List[FixtureResponse])
def list_fixtures(
    limit: int = 100,
    offset: int = 0,
    service: FixtureService = Depends(get_fixture_service)
):
    """Get all fixtures with pagination."""
    return service.list(limit=limit, offset=offset)


@router.get("/{fixture_id}", response_model=FixtureResponse)
def get_fixture(
    fixture_id: int,
    service: FixtureService = Depends(get_fixture_service)
):
    """Get a specific fixture by ID."""
    fixture = service.get(fixture_id)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fixture with ID {fixture_id} not found"
        )
    return fixture


@router.get("/{fixture_id}/details")
def get_fixture_with_details(
    fixture_id: int,
    service: FixtureService = Depends(get_fixture_service)
):
    """Get a fixture with all events, lineups, and statistics."""
    fixture = service.with_events(fixture_id)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fixture with ID {fixture_id} not found"
        )
    return fixture


@router.post("/", response_model=FixtureResponse, status_code=status.HTTP_201_CREATED)
def create_fixture(
    fixture_data: FixtureCreate,
    service: FixtureService = Depends(get_fixture_service)
):
    """Create a new fixture."""
    return service.create(fixture_data)


@router.put("/{fixture_id}", response_model=FixtureResponse)
def update_fixture(
    fixture_id: int,
    fixture_data: FixtureUpdate,
    service: FixtureService = Depends(get_fixture_service)
):
    """Update an existing fixture."""
    fixture = service.update(fixture_id, fixture_data)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fixture with ID {fixture_id} not found"
        )
    return fixture


@router.delete("/{fixture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fixture(
    fixture_id: int,
    service: FixtureService = Depends(get_fixture_service)
):
    """Delete a fixture."""
    fixture = service.delete(fixture_id)
    if not fixture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fixture with ID {fixture_id} not found"
        )
    return None
