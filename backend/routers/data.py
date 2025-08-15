from fastapi import APIRouter, HTTPException, Query
from db.database import supabase
from schemas.climate import HistoricalClimateResponse, HistoricalClimateData
from utils.nasa_api import fetch_historical_climate
from schemas.climate import CurrentWeatherResponse, CurrentWeather, DailyForecast
from utils.openweather_current import fetch_current_weather

from schemas.airquality import AirQualityResponse, AirQuality
from utils.openweather_airquality import fetch_air_quality

data_router = APIRouter(prefix="/data", tags=["Climate Data"])

@data_router.get("/historical", response_model=HistoricalClimateResponse)
def get_historical_climate(
    region_id: int = Query(..., description="ID of the region"),
    start: str = Query(..., description="Start date YYYYMMDD"),
    end: str = Query(..., description="End date YYYYMMDD")
):
    """
    Fetch historical climate data for a given region.
    """
    # Get region coordinates from Supabase
    try:
        region_resp = supabase.table("regions").select("*").eq("id", region_id).execute()
        if not region_resp.data:
            raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
        region = region_resp.data[0]
        lat = region["latitude"]
        lon = region["longitude"]
        name = region["name"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching region: {str(e)}")

    # Fetch data from NASA API
    try:
        climate_data = fetch_historical_climate(lat, lon, start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical data: {str(e)}")

    return HistoricalClimateResponse(
        region_id=region_id,
        region_name=name,
        data=[HistoricalClimateData(**d) for d in climate_data]
    )



#@data_router.get("/current", response_model=CurrentWeatherResponse)
#def get_current_weather(region_id: int = Query(..., description="ID of the region")):
#    """
 #   Fetch current weather for a region.
  #  7-day forecast placeholder will be empty due to Free plan limitations.
  #  """
  #  # Get region coordinates from Supabase
  #  try:
  ##      if not region_resp.data:
    #        raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
    #    region = region_resp.data[0]
    #    lat = region["latitude"]
    ##    name = region["name"]
   ##    raise HTTPException(status_code=500, detail=f"Error fetching region: {str(e)}")
#
 #   # Fetch current weather
  #  try:
   #     current, daily = fetch_current_weather(lat, lon)
   # except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")
#
 #   return CurrentWeatherResponse(
  #      region_id=region_id,
   #     region_name=name,
    #    current=CurrentWeather(**current),
     #   daily=[DailyForecast(**d) for d in daily]  # empty list for now
#    )



@data_router.get("/airquality", response_model=AirQualityResponse)
def get_air_quality(region_id: int = Query(..., description="ID of the region")):
    """
    Fetch air quality for a region using OpenWeather Air Pollution API.
    """
    # Get region coordinates from Supabase
    try:
        region_resp = supabase.table("regions").select("*").eq("id", region_id).execute()
        if not region_resp.data:
            raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
        region = region_resp.data[0]
        lat = region["latitude"]
        lon = region["longitude"]
        name = region["name"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching region: {str(e)}")

    # Fetch air quality from OpenWeather
    try:
        measurement = fetch_air_quality(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching air quality: {str(e)}")

    return AirQualityResponse(
        region_id=region_id,
        region_name=name,
        measurement=AirQuality(**measurement)
    )