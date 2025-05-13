import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app

client = TestClient(app)

def test_create_time_entry():
    """Test creating a new time entry"""
    test_entry = {
        "date": datetime.now().isoformat(),
        "duration_minutes": 30,
        "notes": "Test entry"
    }
    
    # Test user ID (replace with a valid UUID from your Supabase auth)
    test_user_id = "test_user_id"
    
    response = client.post(
        f"/api/v1/time-entries/?user_id={test_user_id}",
        json=test_entry
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["duration_minutes"] == test_entry["duration_minutes"]
    assert data["notes"] == test_entry["notes"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_time_entries():
    """Test getting all time entries for a user"""
    test_user_id = "test_user_id"
    
    response = client.get(f"/api/v1/time-entries/?user_id={test_user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

if __name__ == "__main__":
    pytest.main([__file__]) 