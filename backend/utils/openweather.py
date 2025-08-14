import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_current_weather(lat: float, lon: float):
    """
    Fetch current weather for a location using OpenWeather Free plan.
    Returns:
        - current: dict with temperature, humidity, wind_speed, description
        - daily: empty list placeholder (7-day forecast not available in free plan)
    """
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"OpenWeather API error: {response.status_code}")

    data = response.json()

    current = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }

    daily_forecast = []  # placeholder since Free plan cannot fetch 7-day forecast

    return current, daily_forecast
