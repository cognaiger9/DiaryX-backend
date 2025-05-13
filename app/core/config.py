from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SideProject Tracker"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Supabase settings
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings() 