import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)

# Automatically runs before every new test
@pytest.fixture(autouse=True)
def reset_db():
    main.todo_db.clear()
    main.next_id = 1


def test_create_todo():
    response = client.post("/todos",
                           json={"title":"Learn FastAPI", "priority": "high"}
                           )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "description": None,
        "priority": "high",
        "completed": False,
    }


def test_get_todos_with_filters():
    client.post("/todos", json={"title": "Learn FastAPI", "priority": "high"})
    client.post("/todos", json={"title": "Finish FastAPI", "priority": "low"})

    response = client.get("/todos?priority=high")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Learn FastAPI"

def test_forbid_extra_query_params():
    # Sending an unknown query param should trigger a 422 validation error
    response = client.get("/todos?unknown_filter=123")
    assert response.status_code == 422

def test_todo_by_id():
    client.post("/todos", json={"title": "Read docs"})

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Read docs"

def test_update_todo():
    client.post("/todos", json={"title": "Read docs"})

    response = client.put("/todos/1", json={"title": "Read docs", "completed": True})

    assert response.json()["completed"]

def test_delete_todo():
    client.post("/todos", json={"title": "Read docs"})

    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"Delete Operation": "Success"}

    response2 =client.get("/todos/1")
    assert response2.json() == {"error": "Todo not found"}