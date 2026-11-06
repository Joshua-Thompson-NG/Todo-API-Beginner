import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    main.todo_db.clear()
    main.current_id = 1


def test_create_todo():
    payload = client.post("/todos",
                          json={
                              "title": "Washing Dishes",
                              "description": "Check If I have any dishes to wash today"})

    assert payload.status_code == 201
    assert payload.json()["title"] == "Washing Dishes"
    assert payload.json()["description"] == "Check If I have any dishes to wash today"
    assert not payload.json()["done"]

def test_create_todo_empty_title():
    payload = client.post("/todos",
                          json={"title": "", "description": "Testing"})
    assert payload.status_code == 422


def test_list_all_todos():
    response = client.get("/todos")
    assert response.status_code == 200

def test_get_todo():
    client.post("/todos", json={
                            "title": "Washing Dishes",
                            "description": "Check If I have any dishes to wash today"})
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Washing Dishes"

def test_get_todo_not_found():
    response = client.get("/todos/1")
    assert response.status_code == 404


def test_replace_todo():
    client.post("/todos", json={
                            "title": "Washing Dishes",
                            "description": "Check If I have any dishes to wash today"})
    response = client.put("/todos/1", json={
                            "title": "Doing Chores",
                            "description": "Do list of chores I have",
                            "done":True})
    assert response.status_code == 200
    assert response.json()["title"] == "Doing Chores"


def test_partially_update():
    client.post("/todos", json={
                            "title": "Washing Dishes",
                            "description": "Check If I have any dishes to wash today"})
    response = client.patch("/todos/1", json={
                            "title": "Doing Chores",
                            "description": "Do list of chores I have"})
    assert response.status_code == 200
    assert response.json()["title"] == "Doing Chores"
    assert response.json()["description"] == "Do list of chores I have"

def test_delete_todo():
    client.post(
        "/todos",
        json={
            "title": "Washing Dishes",
            "description": "Check If I have any dishes to wash today",
        },
    )

    response = client.delete("/todos/1")
    assert response.status_code == 204




