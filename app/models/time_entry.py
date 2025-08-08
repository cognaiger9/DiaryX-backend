from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TimeEntryBase(BaseModel):
    date: datetime
    duration_minutes: int = Field(gt=0, description="Duration in minutes")
    notes: str | None = None
    energy: int | None = Field(default=None, ge=1, le=10, description="Energy rating 1–10")
    focus: int | None = Field(default=None, ge=1, le=10, description="Focus rating 1–10")
    project: str | None = None
    tags: list[str] | None = None

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.isoformat()
        }
    )

class TimeEntryQuickAdd(BaseModel):
    """Minimal payload to quickly create a placeholder entry for a given day."""
    date: datetime
    notes: str | None = None

class TimeEntryCreate(TimeEntryBase):
    """Payload for creating/updating a full time entry from the capture modal."""
    pass

class TimeEntry(TimeEntryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat()
        }
    ) 