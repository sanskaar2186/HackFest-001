from pydantic import BaseModel

class AirQuality(BaseModel):
    aqi: int
    pm2_5: float
    pm10: float
    co: float
    no2: float
    o3: float
    so2: float
    nh3: float

class AirQualityResponse(BaseModel):
    region_id: int
    region_name: str
    measurement: AirQuality
