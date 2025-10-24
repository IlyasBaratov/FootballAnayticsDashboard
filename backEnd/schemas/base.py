"""Base schemas for common patterns."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(from_attributes=True)


class TimestampMixin(BaseModel):
    """Mixin for models with timestamps."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
