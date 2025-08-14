from fastapi import APIRouter, HTTPException
from typing import List
from db.database import supabase
from schemas.regions import Region

reg_router = APIRouter(
    prefix="/regions",  # <- all routes start with /regions
    tags=["Regions"]
)
@reg_router.get("/", response_model=List[Region])
def list_regions():
    """
    Returns all regions
    """
    try:
        response = supabase.table("regions").select("*").execute()
        return response.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching regions: {str(e)}")

@reg_router.get("/{region_id}", response_model=Region)
def get_region(region_id: int):
    """
    Returns a single region by its ID
    """
    try:
        response = supabase.table("regions").select("*").eq("id", region_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Region with id {region_id} not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching region: {str(e)}")