#!/usr/bin/env python3
"""
Test script to check if all imports work correctly
Run this to debug import issues
"""

print("Testing imports...")

try:
    print("✓ Importing config...")
    from config import settings
    print(f"  - SUPABASE_URL: {'✓ Set' if settings.SUPABASE_URL else '❌ Missing'}")
    print(f"  - SUPABASE_KEY: {'✓ Set' if settings.SUPABASE_KEY else '❌ Missing'}")
    print(f"  - SECRET_KEY: {'✓ Set' if settings.SECRET_KEY else '❌ Missing'}")
    
    print("\n✓ Importing database...")
    from db.database import supabase, get_db
    print("  - Supabase client created successfully")
    
    print("\n✓ Importing schemas...")
    from schemas.auth import RegisterUser, LoginUser
    print("  - Auth schemas imported successfully")
    
    print("\n✓ Importing models...")
    from models.user import UserResponse, AuthTokens
    print("  - User models imported successfully")
    
    print("\n✓ Importing router...")
    from routers.auth import router
    print("  - Auth router imported successfully")
    
    print("\n✅ All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"  File: {e.__traceback__.tb_frame.f_code.co_filename}")
    print(f"  Line: {e.__traceback__.tb_lineno}")
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
