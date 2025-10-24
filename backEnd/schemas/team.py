"""Team related schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    """Base team schema."""
    name: str
    short_code: Optional[str] = None
    country: Optional[str] = None
    founded: Optional[int] = None
    national: bool = False
    logo: Optional[str] = None
    venue_id: Optional[int] = None


class TeamCreate(TeamBase):
    """Schema for creating a team."""
    id: int


class TeamUpdate(BaseModel):
    """Schema for updating a team."""
    name: Optional[str] = None
    short_code: Optional[str] = None
    country: Optional[str] = None
    founded: Optional[int] = None
    national: Optional[bool] = None
    logo: Optional[str] = None
    venue_id: Optional[int] = None


class TeamResponse(TeamBase):
    """Schema for team response."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
