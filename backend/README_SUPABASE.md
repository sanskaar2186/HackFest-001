# Supabase Integration for HackFest

This document provides instructions for setting up and using Supabase with the HackFest backend.

## Setup Instructions

### 1. Create a Supabase Account and Project

1. Go to [Supabase](https://supabase.com/) and sign up for an account if you don't have one.
2. Create a new project and note down your project URL and API key.

### 2. Set Up Environment Variables

1. Copy the `.env.example` file to a new file named `.env`:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-supabase-api-key
   SECRET_KEY=your-secret-key-for-jwt
   ```

### 3. Create Database Tables

In your Supabase project, create the following tables:

#### Users Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 4. Install Dependencies

Install the required dependencies:

```
pip install -r requirements.txt
```

### 5. Run the Application

Start the FastAPI application:

```
python -m uvicorn main:app --reload
```

## API Endpoints

### Authentication

- **Register**: `POST /auth/register`
  - Request Body: `{"email": "user@example.com", "password": "password123", "username": "username"}`
  - Response: User details

- **Login**: `POST /auth/token`
  - Request Body: `{"username": "user@example.com", "password": "password123"}`
  - Response: Access token

- **Get Current User**: `GET /auth/users/me`
  - Headers: `Authorization: Bearer {token}`
  - Response: User details

## Security Considerations

1. In a production environment, make sure to:
   - Use HTTPS
   - Restrict CORS to specific origins
   - Store passwords securely (Supabase Auth handles this automatically)
   - Use a strong SECRET_KEY for JWT

2. The current implementation uses a simple password comparison. In a real application, you should use Supabase Auth or implement proper password hashing.

## Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JWT Authentication](https://jwt.io/)