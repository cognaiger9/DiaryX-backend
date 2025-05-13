from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TimeEntryBase(BaseModel):
    date: datetime
    duration_minutes: int = Field(gt=0, description="Duration in minutes")
    notes: str | None = None

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.isoformat()
        }
    )

class TimeEntryCreate(TimeEntryBase):
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