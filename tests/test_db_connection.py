import os
from datetime import datetime
from dotenv import load_dotenv
from app.core.supabase import get_supabase_client

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test basic Supabase connection and operations"""
    try:
        # Initialize Supabase client
        supabase = get_supabase_client()
        print("✅ Successfully connected to Supabase")

        # Test data
        test_entry = {
            "date": datetime.now().isoformat(),
            "duration_minutes": 30,
            "notes": "Test entry",
            "user_id": "test_user"
        }

        # Test insert
        print("\nTesting insert operation...")
        result = supabase.table("time_entries").insert(test_entry).execute()
        print("✅ Successfully inserted test entry")
        
        # Get the inserted entry ID
        entry_id = result.data[0]["id"]
        print(f"Inserted entry ID: {entry_id}")

        # Test select
        print("\nTesting select operation...")
        result = supabase.table("time_entries")\
            .select("*")\
            .eq("id", entry_id)\
            .execute()
        print("✅ Successfully retrieved test entry")
        print(f"Retrieved data: {result.data[0]}")

        # Test delete
        print("\nTesting delete operation...")
        result = supabase.table("time_entries")\
            .delete()\
            .eq("id", entry_id)\
            .execute()
        print("✅ Successfully deleted test entry")

        print("\n🎉 All database operations completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise e

if __name__ == "__main__":
    test_supabase_connection() 