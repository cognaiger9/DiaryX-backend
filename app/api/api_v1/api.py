from fastapi import APIRouter
from app.api.api_v1.endpoints import time_entries

api_router = APIRouter()

api_router.include_router(
    time_entries.router,
    prefix="/time-entries",
    tags=["time-entries"]
) 