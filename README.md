# Todo API Beginner

A simple FastAPI project for managing todos. This project was built as a beginner-friendly API to practice CRUD operations, request validation, filtering, and testing with FastAPI.

## Features
- Create a todo
- Get all todos
- Filter todos by completed status, priority, and search term
- Get a todo by ID
- Update a todo
- Delete a todo
- Automated tests using FastAPI's TestClient

## Tech Stack
- Python
- FastAPI
- Pytest

## Project Structure
```bash
.
├── main.py
├── test_main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

## Requirements
Make sure you have Python 3.13+ installed.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate   # On macOS/Linux
# or
.venv\Scripts\activate      # On Windows
pip install -r requirements.txt
```

If you are using `uv`, you can also run:
```bash
uv sync
```

## Run the API
```bash
uvicorn main:app --reload
```

Then open:
```bash
http://127.0.0.1:8000/docs
```

## API Endpoints

### Create a todo
```bash
curl -X POST "http://127.0.0.1:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI","priority":"high"}'
```

### Get all todos
```bash
curl "http://127.0.0.1:8000/todos"
```

### Filter todos
```bash
curl "http://127.0.0.1:8000/todos?priority=high"
```

### Get a todo by ID
```bash
curl "http://127.0.0.1:8000/todos/1"
```

### Update a todo
```bash
curl -X PUT "http://127.0.0.1:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI","completed":true}'
```

### Delete a todo
```bash
curl -X DELETE "http://127.0.0.1:8000/todos/1"
```

## Running Tests
```bash
pytest
```

## Notes
This project currently uses an in-memory dictionary instead of a database, which is a great beginner approach for learning API structure and validation before adding SQLite or an ORM.

## Next Improvements
- Return proper HTTP status codes
- Connect to SQLite or a database
- Organize code into separate modules as the project grows