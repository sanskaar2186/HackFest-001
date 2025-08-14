from pydantic import BaseModel
from typing import List, Dict

class HistoricalClimateData(BaseModel):
    date: str  # e.g., "2023-08-14"
    temperature: float  # avg temp in °C
    precipitation: float  # mm
    # add other fields if needed

class HistoricalClimateResponse(BaseModel):
    region_id: int
    region_name: str
    data: List[HistoricalClimateData]
