# schemas/forecast.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal

class Scenario(BaseModel):
    temp_delta: float = 0.0
    rain_delta: float = 0.0

class ForecastRequest(BaseModel):
    region_id: int
    horizon_days: int = Field(..., description="Number of future days to forecast (e.g., 7 or 14)")
    scenario: Optional[Scenario] = None

    @validator("horizon_days")
    def _check_horizon(cls, v):
        if v <= 0:
            raise ValueError("horizon_days must be > 0")
        if v > 30:
            # keep forecasts light; Prophet can do more, but 30 is a sensible cap
            raise ValueError("horizon_days must be <= 30")
        return v

class ForecastDay(BaseModel):
    date: str
    temperature: float
    temperature_ci_low: float
    temperature_ci_high: float
    rainfall: float
    rainfall_ci_low: float
    rainfall_ci_high: float

class ForecastResponse(BaseModel):
    region_id: int
    region_name: str
    forecast: List[ForecastDay]

# ---- Training request/response ----

class TrainClimateRequest(BaseModel):
    # If omitted or empty, we’ll train ALL regions found in the DB
    region_ids: Optional[List[int]] = None
    start_date: Optional[str] = None  # "YYYY-MM-DD", default "2010-01-01"
    end_date: Optional[str] = None    # "YYYY-MM-DD"

class TrainResult(BaseModel):
    region_id: int
    status: Literal["success", "error"]
    records_used: Optional[int] = None
    model_path: Optional[str] = None
    message: Optional[str] = None

class TrainClimateResponse(BaseModel):
    status: Literal["completed"]
    results: List[TrainResult]
