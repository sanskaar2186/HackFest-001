# routers/forecast.py
from fastapi import APIRouter, HTTPException
from db.database import supabase
from schemas.forecast import ForecastRequest, ForecastResponse, ForecastDay
from ml_models.climate_train import has_trained_model, train_climate_model
from ml_models.climate_predict import forecast_region, apply_scenario

router = APIRouter(tags=["Climate Forecast"])

@router.post("/forecast/climate", response_model=ForecastResponse)
def forecast_climate(req: ForecastRequest):
    # 1) region lookup
    r = supabase.table("regions").select("*").eq("id", req.region_id).single().execute()
    if not r.data:
        raise HTTPException(status_code=404, detail="Region not found")

    region = r.data
    lat, lon = region.get("latitude"), region.get("longitude")
    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Region coordinates missing")

    # 2) ensure a model exists (train on-demand if missing)
    if not has_trained_model(req.region_id):
        try:
            # Start from 2015 to keep the artifact lighter/faster; adjust if you want the full range
            train_climate_model(req.region_id, float(lat), float(lon), start_date="2015-01-01")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Training failed: {e}")

    # 3) forecast
    try:
        fc = forecast_region(req.region_id, req.horizon_days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast failed: {e}")

    # 4) optional scenario adjust
    if req.scenario:
        fc = apply_scenario(fc, temp_delta=req.scenario.temp_delta, rain_delta=req.scenario.rain_delta)

    # 5) response mapping
    return ForecastResponse(
        region_id=region["id"],
        region_name=region["name"],
        forecast=[ForecastDay(**row) for row in fc]
    )

@router.post("/forecast/scenario", response_model=ForecastResponse)
def forecast_scenario(req: ForecastRequest):
    # Reuse the same flow; scenario in body will adjust
    return forecast_climate(req)
