from fastapi import APIRouter, HTTPException
from typing import List
from app.models.time_entry import TimeEntry, TimeEntryCreate
from app.core.supabase import supabase

router = APIRouter()

@router.post("/", response_model=TimeEntry)
async def create_time_entry(entry: TimeEntryCreate):
    """
    Create a new time entry.
    
    Args:
        entry: TimeEntryCreate object containing date, duration, and notes
    
    Returns:
        TimeEntry: The created time entry
    """
    try:
        # Prepare the data for insertion
        data = entry.model_dump()
        data["date"] = data["date"].isoformat()
        
        # Insert the entry into the database
        result = supabase.table("time_entries").insert(data).execute()
        
        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to create time entry")
            
        return result.data[0]
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error creating time entry: {str(e)}"
        )

@router.get("/", response_model=List[TimeEntry])
async def get_time_entries():
    """
    Get all time entries.
    
    Returns:
        List[TimeEntry]: List of time entries
    """
    try:
        result = supabase.table("time_entries")\
            .select("*")\
            .order("date", desc=True)\
            .execute()
            
        return result.data
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching time entries: {str(e)}"
        )

@router.get("/{entry_id}", response_model=TimeEntry)
async def get_time_entry(entry_id: int):
    """
    Get a specific time entry by ID.
    
    Args:
        entry_id: The ID of the time entry to retrieve
    
    Returns:
        TimeEntry: The requested time entry
    """
    try:
        result = supabase.table("time_entries")\
            .select("*")\
            .eq("id", entry_id)\
            .execute()
            
        if not result.data:
            raise HTTPException(status_code=404, detail="Time entry not found")
            
        return result.data[0]
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching time entry: {str(e)}"
        ) 