# database.py
from supabase import create_client, Client
from config import settings

if not settings.SUPABASE_URL  or not settings.SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("Supabase credentials are missing. Check your .env file.")

# Create Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

def get_db() -> Client:
    """Get database client"""
    return supabase
