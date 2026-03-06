# AGENTS.md — Python FastAPI Project

## Stack
- Python 3.12+
- FastAPI + Uvicorn
- SQLAlchemy 2.0 + Alembic (migrations)
- Pydantic v2 for validation
- Poetry for dependency management

## Code Style
- Follow PEP 8
- Use type hints everywhere
- Use `async def` for all endpoint handlers
- Docstrings: Google style

## Project Structure
```
app/
├── main.py           # FastAPI app instance
├── routers/          # API route modules
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── dependencies.py   # Dependency injection
└── config.py         # Settings (pydantic-settings)
```

## Commands
- Run: `poetry run uvicorn app.main:app --reload`
- Test: `poetry run pytest -v`
- Lint: `poetry run ruff check .`
- Format: `poetry run ruff format .`
- Migrate: `poetry run alembic upgrade head`

## Rules
- Never use `*` imports
- Always use dependency injection for DB sessions
- Endpoints must have response_model defined
- Use HTTPException for error responses, not bare raises
- Sensitive config via environment variables only (never hardcode)
- Write tests for every new endpoint
