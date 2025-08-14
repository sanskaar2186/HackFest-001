from pydantic import BaseModel

class AnomalyRequest(BaseModel):
    region_id: int

class AnomalyResponse(BaseModel):
    region_id: int
    region_name: str
    delta_temp: float
    delta_rainfall: float
    delta_aqi: float
