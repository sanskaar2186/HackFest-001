# database.py
from supabase import create_client
from .config import settings

# Initialize Supabase client
def get_supabase_client():
    """Create and return a Supabase client instance"""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Supabase URL and API key must be provided in environment variables")
    
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# User-related database functions
def get_user_by_email(email: str):
    """Get a user by email from Supabase"""
    supabase = get_supabase_client()
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None

def get_user_by_id(user_id: str):
    """Get a user by ID from Supabase"""
    supabase = get_supabase_client()
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data[0] if response.data else None

def create_user(user_data: dict):
    """Create a new user in Supabase"""
    supabase = get_supabase_client()
    response = supabase.table("users").insert(user_data).execute()
    return response.data[0] if response.data else None

# Add more database functions as needed for your application
# For example: update_user, delete_user, get_hackathons, etc.