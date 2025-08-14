# HackFest Backend - Fixed Authentication System

## What's Fixed

✅ **Import errors** - Fixed relative import issues  
✅ **Missing schemas** - Created auth.py schemas  
✅ **Database connection** - Fixed get_db function  
✅ **Router imports** - Fixed import paths in main.py  

## Quick Setup

### 1. Environment Variables
Create `.env` file:
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_anon_key_here
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=0.0.0.0
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python main.py
```

## API Endpoints

- `POST /register` - User registration
- `POST /login` - User login  
- `GET /test-db` - Test database connection

## Test the System

1. **Test Database**: `http://localhost:8000/test-db`
2. **Register User**: `POST /register` with email, username, password
3. **Login User**: `POST /login` with email, password

## Folder Structure

```
backend/
├── models/          # User models
│   └── user.py     
├── schemas/         # Request/response schemas
│   └── auth.py     
├── routers/         # API endpoints
│   └── auth.py     
├── db/             # Database connection
│   └── database.py 
├── config.py       # Settings
└── main.py         # FastAPI app
```

## Example Requests

### Register
```json
{
  "email": "user@example.com",
  "username": "testuser",
  "password": "SecurePass123"
}
```

### Login
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

Your authentication system should now work without errors!