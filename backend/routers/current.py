from fastapi import APIRouter, HTTPException, Query
from db.database import supabase
from utils.openweather_current import fetch_current_weather
from schemas.climate import CurrentWeather, CurrentWeatherResponse, DailyForecast

current_router = APIRouter(tags=["Current Weather"])

@current_router.get("/current", response_model=CurrentWeatherResponse)
def get_current_weather(region_id: int = Query(..., description="ID of the region")):
    # 1️⃣ Fetch region info
    region_resp = supabase.table("regions").select("*").eq("id", region_id).execute()
    if not region_resp.data:
        raise HTTPException(status_code=404, detail="Region not found")
    region = region_resp.data[0]

    lat = region.get("latitude")
    lon = region.get("longitude")
    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Region coordinates missing")

    # 2️⃣ Fetch weather
    weather_dict = fetch_current_weather(lat, lon)

    # 3️⃣ Map to CurrentWeather Pydantic model
    current_weather = CurrentWeather(**weather_dict)

    # 4️⃣ Return as CurrentWeatherResponse
    return CurrentWeatherResponse(
        region_id=region.get("id"),
        region_name=region.get("name"),
        current=current_weather,
        daily=[]  # free plan limitation
    )
