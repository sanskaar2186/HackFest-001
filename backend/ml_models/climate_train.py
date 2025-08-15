# ml_models/climate_train.py
import requests
import pandas as pd
from prophet import Prophet
import joblib
from datetime import date
from typing import Tuple
from io import BytesIO

from db.database import supabase  # <- your existing Supabase client

BUCKET_NAME = "climate-models"  # make sure this bucket exists in Supabase Storage

def _object_name(region_id: int) -> str:
    # Keep it simple; you can also prefix with a folder if you want
    return f"region_{region_id}.pkl"

def _fetch_open_meteo(lat: float, lon: float, start_date: str, end_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns two dataframes:
      - df_temp: columns [ds, y] -> daily max temperature
      - df_rain: columns [ds, y] -> daily precipitation sum
    """
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&daily=temperature_2m_max,precipitation_sum"
        "&timezone=auto"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if "daily" not in data or not data["daily"].get("time"):
        raise ValueError("No historical data from API")

    days = pd.to_datetime(data["daily"]["time"])
    df_temp = pd.DataFrame({"ds": days, "y": data["daily"]["temperature_2m_max"]})
    df_rain = pd.DataFrame({"ds": days, "y": data["daily"]["precipitation_sum"]})
    return df_temp, df_rain

def train_climate_model(
    region_id: int,
    lat: float,
    lon: float,
    start_date: str = "2010-01-01",
    end_date: str | None = None
) -> dict:
    """
    Trains two Prophet models (temperature max, precipitation sum),
    packs them into one joblib bundle, and uploads to Supabase Storage.
    """
    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")

    df_temp, df_rain = _fetch_open_meteo(lat, lon, start_date, end_date)

    m_temp = Prophet(daily_seasonality=True, yearly_seasonality=True)
    m_temp.fit(df_temp)

    m_rain = Prophet(daily_seasonality=True, yearly_seasonality=True)
    m_rain.fit(df_rain)

    bundle = {
        "temp_model": m_temp,
        "rain_model": m_rain,
        "trained_until": end_date
    }

    buf = BytesIO()
    joblib.dump(bundle, buf)
    buf.seek(0)
    content = buf.getvalue()

    # Upload to Supabase (overwrite if exists)
    supabase.storage.from_(BUCKET_NAME).upload(
        path=_object_name(region_id),
        file=content,
        file_options={"contentType": "application/octet-stream", "upsert": "true"}
    )

    return {
        "records_used": min(len(df_temp), len(df_rain)),
        "model_path": f"supabase://{BUCKET_NAME}/{_object_name(region_id)}"
    }

def has_trained_model(region_id: int) -> bool:
    """
    Checks if model exists in the Supabase bucket.
    """
    try:
        files = supabase.storage.from_(BUCKET_NAME).list()
        return any((f.get("name") == _object_name(region_id)) for f in files)
    except Exception:
        return False
