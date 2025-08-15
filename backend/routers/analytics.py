from fastapi import APIRouter, HTTPException
from db.database import supabase
from schemas.anomaly import AnomalyRequest, AnomalyResponse
from utils.openweather_current import fetch_current_weather

from utils.openweather_airquality import fetch_air_quality
import logging

analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])
logging.basicConfig(level=logging.INFO)

# Mock baseline data (replace later with real historical averages)
BASELINE = {
    "temperature": 25.0,  # °C
    "rainfall": 100.0,    # mm
    "aqi": 50             # AQI
}

@analytics_router.post("/anomaly", response_model=AnomalyResponse)
def compute_anomaly(request: AnomalyRequest):
    try:
        # 1️⃣ Get region from Supabase
        region_resp = supabase.table("regions").select("*").eq("id", request.region_id).execute()
        logging.info(f"Supabase response: {region_resp.data}")
        if not region_resp.data:
            raise HTTPException(status_code=404, detail="Region not found")
        region = region_resp.data[0]
        lat = region.get("latitude")
        lon = region.get("longitude")
        name = region.get("name")
        if lat is None or lon is None:
            raise HTTPException(status_code=400, detail="Region coordinates missing")
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.exception("Error fetching region")
        raise HTTPException(status_code=500, detail=f"Error fetching region: {str(e)}")

    try:
        # 2️⃣ Fetch current weather
        weather = fetch_current_weather(lat, lon)
        logging.info(f"Current weather: {weather}")
        if not weather or "temperature" not in weather or "rainfall" not in weather:
            raise HTTPException(status_code=500, detail="Weather data incomplete")
    except Exception as e:
        logging.exception("Error fetching weather")
        raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")

    try:
        # 3️⃣ Fetch current air quality
        air = fetch_air_quality(lat, lon)
        logging.info(f"Air quality: {air}")
        if not air or "aqi" not in air:
            raise HTTPException(status_code=500, detail="Air quality data incomplete")
    except Exception as e:
        logging.exception("Error fetching air quality")
        raise HTTPException(status_code=500, detail=f"Error fetching air quality: {str(e)}")

    try:
        # 4️⃣ Compute anomalies
        delta_temp = weather["temperature"] - BASELINE["temperature"]
        delta_rainfall = weather["rainfall"] - BASELINE["rainfall"]
        delta_aqi = air["aqi"] - BASELINE["aqi"]
    except Exception as e:
        logging.exception("Error computing anomalies")
        raise HTTPException(status_code=500, detail=f"Error computing anomalies: {str(e)}")

    return AnomalyResponse(
        region_id=request.region_id,
        region_name=name,
        delta_temp=round(delta_temp, 2),
        delta_rainfall=round(delta_rainfall, 2),
        delta_aqi=round(delta_aqi, 2)
    )
