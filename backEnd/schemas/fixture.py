"""Fixture related schemas."""
from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class FixtureBase(BaseModel):
    """Base fixture schema."""
    league_id: Optional[int] = None
    season_id: Optional[str] = None
    round_id: Optional[str] = None
    group_id: Optional[str] = None
    venue_id: Optional[int] = None
    referee: Optional[str] = None
    event_date: Optional[datetime] = None
    status: Optional[str] = None
    status_code: Optional[int] = None
    home_team_id: int
    away_team_id: int
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    winner: Optional[int] = None
    round_name: Optional[str] = None
    attendance: Optional[int] = None


class FixtureCreate(FixtureBase):
    """Schema for creating a fixture."""
    id: int


class FixtureUpdate(BaseModel):
    """Schema for updating a fixture."""
    status: Optional[str] = None
    status_code: Optional[int] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    winner: Optional[int] = None
    attendance: Optional[int] = None


class FixtureResponse(FixtureBase):
    """Schema for fixture response."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class FixtureDetailResponse(FixtureResponse):
    """Schema for detailed fixture response with events and stats."""
    events: list[dict] = []
    lineups: list[dict] = []
    player_stats: list[dict] = []
    team_stats: list[dict] = []
