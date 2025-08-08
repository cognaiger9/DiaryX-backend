from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from app.models.time_entry import TimeEntry, TimeEntryCreate, TimeEntryQuickAdd
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
async def get_time_entries(
    start_date: datetime | None = Query(None, description="Filter entries from this date (inclusive)"),
    end_date: datetime | None = Query(None, description="Filter entries up to this date (inclusive)"),
):
    """
    Get all time entries.
    
    Returns:
        List[TimeEntry]: List of time entries
    """
    try:
        query = (
            supabase
            .table("time_entries")
            .select("*")
        )
        if start_date is not None:
            query = query.gte("date", start_date.isoformat())
        if end_date is not None:
            query = query.lte("date", end_date.isoformat())

        result = query.order("date", desc=True).execute()
            
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
        result = (
            supabase.table("time_entries")
            .select("*")
            .eq("id", entry_id)
            .execute()
        )
            
        if not result.data:
            raise HTTPException(status_code=404, detail="Time entry not found")
            
        return result.data[0]
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching time entry: {str(e)}"
        ) 

@router.post("/quick-add", response_model=TimeEntry)
async def quick_add_time_entry(payload: TimeEntryQuickAdd):
    """
    Quick add a time entry with minimal fields. Defaults `duration_minutes` to 1
    so the entry is valid, allowing the frontend to update it later.

    This supports clicking a day cell to seed an entry for that date.
    """
    try:
        data = {
            "date": payload.date.isoformat(),
            "duration_minutes": 1,
            "notes": payload.notes,
        }
        result = supabase.table("time_entries").insert(data).execute()
        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to quick add time entry")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error quick adding time entry: {str(e)}")

@router.delete("/{entry_id}")
async def delete_time_entry(entry_id: int):
    """Delete a time entry by id for the given user."""
    try:
        # Ensure entry exists and belongs to user
        existing = (
            supabase.table("time_entries").select("id").eq("id", entry_id).execute()
        )
        if not existing.data:
            raise HTTPException(status_code=404, detail="Time entry not found")

        result = (
            supabase.table("time_entries").delete().eq("id", entry_id).execute()
        )
        if result.data is None:
            # Some drivers return no data on delete; consider it success
            return {"status": "deleted"}
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting time entry: {str(e)}")

@router.put("/{entry_id}", response_model=TimeEntry)
async def update_time_entry(
    entry_id: int,
    entry: TimeEntryCreate,
):
    """Update an existing time entry for a user."""
    try:
        # Ensure entry exists and belongs to user
        existing = (
            supabase.table("time_entries").select("id").eq("id", entry_id).execute()
        )
        if not existing.data:
            raise HTTPException(status_code=404, detail="Time entry not found")

        data = entry.model_dump()
        data["date"] = data["date"].isoformat()
        result = (
            supabase.table("time_entries").update(data).eq("id", entry_id).execute()
        )
        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to update time entry")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating time entry: {str(e)}")