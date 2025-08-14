from fastapi import APIRouter, HTTPException
from db.database import supabase
from schemas.anomaly import AnomalyRequest, AnomalyResponse
from utils.openweather import fetch_current_weather
from utils.openweather_airquality import fetch_air_quality

analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Mock baseline data (in real app, fetch from historical DB or NASA POWER)
BASELINE = {
    "temperature": 25.0,  # °C
    "rainfall": 100.0,    # mm
    "aqi": 50             # AQI
}

@analytics_router.post("/anomaly", response_model=AnomalyResponse)
def compute_anomaly(request: AnomalyRequest):
    # Get region from DB
    try:
        region_resp = supabase.table("regions").select("*").eq("id", request.region_id).execute()
        if not region_resp.data:
            raise HTTPException(status_code=404, detail="Region not found")
        region = region_resp.data[0]
        lat = region["latitude"]
        lon = region["longitude"]
        name = region["name"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching region: {str(e)}")

    # Fetch current weather
    try:
        weather = fetch_current_weather(lat, lon)  # should return {"temperature": ..., "rainfall": ...}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")

    # Fetch current AQI
    try:
        air = fetch_air_quality(lat, lon)  # returns {"aqi": ...}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching air quality: {str(e)}")

    # Compute anomalies
    delta_temp = weather["temperature"] - BASELINE["temperature"]
    delta_rainfall = weather["rainfall"] - BASELINE["rainfall"]
    delta_aqi = air["aqi"] - BASELINE["aqi"]

    return AnomalyResponse(
        region_id=request.region_id,
        region_name=name,
        delta_temp=round(delta_temp, 2),
        delta_rainfall=round(delta_rainfall, 2),
        delta_aqi=round(delta_aqi, 2)
    )
