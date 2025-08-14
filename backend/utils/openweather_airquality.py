import os
import requests

BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

def fetch_air_quality(lat: float, lon: float):
    """
    Fetch current air quality using OpenWeather Air Pollution API.
    Returns AQI and pollutants (PM2.5, PM10, CO, NO2, O3, SO2, NH3).
    """
    api_key = os.getenv("OPENWEATHER_KEY")
    if not api_key:
        raise ValueError("API key is missing. Please set OPENWEATHER_API_KEY environment variable.")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"OpenWeather API error: {response.status_code}")

    data = response.json()
    if "list" not in data or not data["list"]:
        raise Exception("No air quality data available for these coordinates")

    measurement = data["list"][0]
    main = measurement.get("main", {})
    components = measurement.get("components", {})

    result = {
        "aqi": main.get("aqi"),
        "pm2_5": components.get("pm2_5"),
        "pm10": components.get("pm10"),
        "co": components.get("co"),
        "no2": components.get("no2"),
        "o3": components.get("o3"),
        "so2": components.get("so2"),
        "nh3": components.get("nh3")
    }

    return result
