# ml_models/climate_predict.py
import joblib
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
from typing import List, Dict

from db.database import supabase
from ml_models.climate_train import BUCKET_NAME, _object_name

# very simple in-memory cache to avoid repeated downloads in one process
_MODEL_CACHE: dict[int, dict] = {}

def _download_bundle(region_id: int) -> dict:
    """
    Download model bundle from Supabase and return the loaded object.
    Caches in memory for the lifetime of the process.
    """
    if region_id in _MODEL_CACHE:
        return _MODEL_CACHE[region_id]

    path = _object_name(region_id)
    resp = supabase.storage.from_(BUCKET_NAME).download(path)
    # supabase-py returns raw bytes for download
    content = resp if isinstance(resp, (bytes, bytearray)) else getattr(resp, "content", None)
    if content is None:
        # some clients may return dict
        if isinstance(resp, dict) and "data" in resp and isinstance(resp["data"], (bytes, bytearray)):
            content = resp["data"]
        else:
            raise FileNotFoundError(f"Could not download model for region {region_id}")

    bundle = joblib.load(BytesIO(content))
    _MODEL_CACHE[region_id] = bundle
    return bundle

def forecast_region(region_id: int, horizon_days: int) -> List[Dict]:
    """
    Returns list of dicts:
      {date, temperature, temperature_ci_low, temperature_ci_high,
       rainfall, rainfall_ci_low, rainfall_ci_high}
    """
    bundle = _download_bundle(region_id)
    m_temp = bundle["temp_model"]
    m_rain = bundle["rain_model"]

    # build the future dataframe from tomorrow for horizon_days
    start_date = (datetime.utcnow().date() + timedelta(days=1))
    future_dates = pd.date_range(start=start_date, periods=horizon_days, freq="D")
    future_df = pd.DataFrame({"ds": future_dates})

    temp_fc = m_temp.predict(future_df)
    rain_fc = m_rain.predict(future_df)

    out: List[Dict] = []
    for i, ts in enumerate(future_dates):
        out.append({
            "date": ts.strftime("%Y-%m-%d"),
            "temperature": float(temp_fc.loc[i, "yhat"]),
            "temperature_ci_low": float(temp_fc.loc[i, "yhat_lower"]),
            "temperature_ci_high": float(temp_fc.loc[i, "yhat_upper"]),
            "rainfall": max(0.0, float(rain_fc.loc[i, "yhat"])),
            "rainfall_ci_low": max(0.0, float(rain_fc.loc[i, "yhat_lower"])),
            "rainfall_ci_high": max(0.0, float(rain_fc.loc[i, "yhat_upper"])),
        })
    return out

def apply_scenario(
    forecast: List[Dict],
    temp_delta: float = 0.0,
    rain_delta: float = 0.0
) -> List[Dict]:
    adj: List[Dict] = []
    for row in forecast:
        adj.append({
            **row,
            "temperature": row["temperature"] + temp_delta,
            "temperature_ci_low": row["temperature_ci_low"] + temp_delta,
            "temperature_ci_high": row["temperature_ci_high"] + temp_delta,
            "rainfall": max(0.0, row["rainfall"] + rain_delta),
            "rainfall_ci_low": max(0.0, row["rainfall_ci_low"] + rain_delta),
            "rainfall_ci_high": max(0.0, row["rainfall_ci_high"] + rain_delta),
        })
    return adj
