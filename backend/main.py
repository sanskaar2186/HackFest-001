# main.py
from fastapi import FastAPI, Request, routing
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from config import settings
from db.database import supabase

app = FastAPI(
    title="HackFest API",
    description="API for HackFest platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routers.auth import router as auth_router
from routers.regions import reg_router as regions_router
from routers.data import data_router
from routers.analytics import analytics_router
from routers.current import current_router



app.include_router(auth_router, prefix="/auth")
app.include_router(regions_router)
app.include_router(data_router)
app.include_router(analytics_router)
app.include_router(current_router)



@app.get("/")
async def root():
    return {"message": "welcome to the Climate vista"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
