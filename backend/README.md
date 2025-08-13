# Backend Server

Python FastAPI backend server.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- virtualenv or venv

## Setup

1. Create and activate virtual environment:
```bash
python -m venv hackfest
source hackfest/bin/activate  # On Windows: hackfest\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the development server:
```bash
python main.py
```

## Project Structure

```
backend/
├── core/           # Core functionality and configurations
├── data/           # Data files
├── db/             # Database models and connections
├── ml_models/      # Machine learning models
├── models/         # Data models/schemas
├── routers/        # API routes
├── schemas/        # Pydantic schemas
├── services/       # Business logic
├── tests/          # Unit tests
└── main.py        # Application entry point
```

## API Documentation

When the server is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

```bash
pytest
```