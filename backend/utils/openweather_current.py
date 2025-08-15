import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_current_weather(lat: float, lon: float) -> dict:
    """
    Fetch current weather for given coordinates.
    Returns a single dictionary with:
        - temperature
        - humidity
        - wind_speed
        - description
        - rainfall
    """
    if not API_KEY:
        raise ValueError("OPENWEATHER_KEY not set in environment")

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
        "temperature": data.get("main", {}).get("temp", 0.0),
        "humidity": data.get("main", {}).get("humidity", 0),
        "wind_speed": data.get("wind", {}).get("speed", 0.0),
        "description": data.get("weather", [{}])[0].get("description", ""),
        "rainfall": data.get("rain", {}).get("1h", 0.0)
    }

    return current  # ✅ single dict only
