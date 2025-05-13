from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from pydantic import BaseModel
from app.core.supabase import supabase

router = APIRouter()

class TimeEntryBase(BaseModel):
    date: datetime
    duration_minutes: int
    notes: str

class TimeEntryCreate(TimeEntryBase):
    pass

class TimeEntry(TimeEntryBase):
    id: int
    user_id: str

    class Config:
        from_attributes = True

@router.post("/", response_model=TimeEntry)
async def create_time_entry(entry: TimeEntryCreate, user_id: str):
    try:
        data = entry.model_dump()
        data["user_id"] = user_id
        result = supabase.table("time_entries").insert(data).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TimeEntry])
async def get_time_entries(user_id: str):
    try:
        result = supabase.table("time_entries")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{entry_id}", response_model=TimeEntry)
async def get_time_entry(entry_id: int, user_id: str):
    try:
        result = supabase.table("time_entries")\
            .select("*")\
            .eq("id", entry_id)\
            .eq("user_id", user_id)\
            .execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Time entry not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 