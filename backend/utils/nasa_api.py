import requests

def fetch_historical_climate(lat: float, lon: float, start: str, end: str):
    """
    Fetch historical climate data from NASA POWER API.
    Parameters:
        lat, lon: coordinates
        start, end: YYYYMMDD format
    Returns:
        List of dicts with date, temperature, precipitation
    """
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "start": start,
        "end": end,
        "latitude": lat,
        "longitude": lon,
        "community": "AG",
        "parameters": "T2M,PRECTOT",
        "format": "JSON"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"NASA API error: {response.status_code}")

    json_data = response.json()
    results = []
    daily_data = json_data.get("properties", {}).get("parameter", {})
    temps = daily_data.get("T2M", {})
    precs = daily_data.get("PRECTOT", {})

    for date, temp in temps.items():
        prec = precs.get(date, 0)
        results.append({
            "date": date,
            "temperature": temp,
            "precipitation": prec
        })

    return results
