# main.py
from fastapi import FastAPI, Request, routing
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os
load_dotenv()

# Import routers
from routers import auth

# Create FastAPI app
app = FastAPI(
    title="HackFest API",
    description="API for HackFest platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],  # In production, replace with specific origins
    allow_origin_regex=os.getenv("FRONTEND_URL"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)