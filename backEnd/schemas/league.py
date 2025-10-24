"""League related schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LeagueBase(BaseModel):
    """Base league schema."""
    name: str
    country: Optional[str] = None
    country_code: Optional[str] = None
    logo: Optional[str] = None
    flag: Optional[str] = None
    type: Optional[str] = None


class LeagueCreate(LeagueBase):
    """Schema for creating a league."""
    id: int


class LeagueUpdate(BaseModel):
    """Schema for updating a league."""
    name: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    logo: Optional[str] = None
    flag: Optional[str] = None
    type: Optional[str] = None


class LeagueResponse(LeagueBase):
    """Schema for league response."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
