# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import risk, community, data

app = FastAPI(title="AZ Outbreak Radar API")

# Allow Streamlit frontend to call this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect all routes
app.include_router(risk.router)
app.include_router(community.router)
app.include_router(data.router)

@app.get("/")
def root():
    return {"status": "AZ Outbreak Radar API is running"}