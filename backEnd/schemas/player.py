"""Player related schemas."""
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class PlayerBase(BaseModel):
    """Base player schema."""
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    name: Optional[str] = None
    nationality: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    photo: Optional[str] = None


class PlayerCreate(PlayerBase):
    """Schema for creating a player."""
    id: int


class PlayerUpdate(BaseModel):
    """Schema for updating a player."""
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    name: Optional[str] = None
    nationality: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    photo: Optional[str] = None


class PlayerResponse(PlayerBase):
    """Schema for player response."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
