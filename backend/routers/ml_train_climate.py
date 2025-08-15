# routers/ml_train_climate.py
from time import sleep
from fastapi import APIRouter, HTTPException
from db.database import supabase
from schemas.forecast import TrainClimateRequest, TrainClimateResponse, TrainResult
from ml_models.climate_train import train_climate_model

router = APIRouter(tags=["ML Training"])

@router.post("/ml/train/climate", response_model=TrainClimateResponse)
def ml_train_climate(body: TrainClimateRequest):
    """
    Train models for a list of region_ids. If region_ids is empty or omitted,
    it will train ALL regions found in the DB.
    """
    # Pull all regions once
    r = supabase.table("regions").select("*").execute()
    if not r.data:
        raise HTTPException(status_code=404, detail="No regions found")

    region_map = {row["id"]: row for row in r.data}

    # decide which IDs to process
    if body.region_ids and len(body.region_ids) > 0:
        region_ids = body.region_ids
    else:
        region_ids = list(region_map.keys())

    results: list[TrainResult] = []

    for rid in region_ids:
        reg = region_map.get(rid)
        if not reg:
            results.append(TrainResult(region_id=rid, status="error", message="Region not found"))
            continue

        lat, lon = reg.get("latitude"), reg.get("longitude")
        if lat is None or lon is None:
            results.append(TrainResult(region_id=rid, status="error", message="Missing coordinates"))
            continue

        try:
            metrics = train_climate_model(
                region_id=rid,
                lat=float(lat),
                lon=float(lon),
                start_date=body.start_date or "2010-01-01",
                end_date=body.end_date
            )
            results.append(TrainResult(
                region_id=rid,
                status="success",
                records_used=metrics["records_used"],
                model_path=metrics["model_path"]
            ))
        except Exception as e:
            results.append(TrainResult(region_id=rid, status="error", message=str(e)))

        # Be nice to Open-Meteo (rate limits). Tune if you hit 429s.
        sleep(1.0)

    return TrainClimateResponse(status="completed", results=results)
