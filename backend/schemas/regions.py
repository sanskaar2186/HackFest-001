from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RegionBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    description: Optional[str] = None

class Region(RegionBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

