from fastapi import FastAPI, Query, Path, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal, Annotated

app = FastAPI()

# Fake Database
todo_db = {}
next_id = 1

# Request Model when sending a request
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, examples=["Washing Dishes"])
    description: str | None = Field(default=None, examples=["Check If I have any dishes to wash today"])
    priority: Literal["low", "medium", "high"] = "low"
    completed: bool = False

# Response Model, what a response is meant to look like
class TodoRead(BaseModel):
    id : int
    title: str
    description: str | None = None
    priority: Literal["low", "medium", "high"]
    completed: bool


class TodoFilterParam(BaseModel):
    model_config = {"extra": "forbid"}

    completed: bool | None = None
    priority: Literal["low", "medium", "high"] | None = None
    search: str | None = None
@app.post("/todos", response_model=TodoRead, status_code=status.HTTP_201_CREATED    )
def create_todo(todo: TodoCreate):
    global next_id

    todo_db[next_id] = todo
    response = {"id":next_id, **todo.model_dump()}
    next_id += 1
    return response
@app.get("/todos")
def get_todos(filters: Annotated[TodoFilterParam, Query()]):
    results = []

    for todo_id, todo in todo_db.items():
        if filters.completed is not None and todo.completed != filters.completed:
            continue

        if filters.priority is not None and todo.priority != filters.priority:
            continue

        if filters.search is not None:
            search_term = filters.search.lower()
            in_title = search_term in todo.title.lower()
            in_desc = todo.description and search_term in todo.description.lower()
            if not in_title and not in_desc:
                continue

        results.append({"id": todo_id, **todo.model_dump()})
    return results


@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todos_id (todo_id: Annotated[int, Path(ge=1)]):
    result = todo_db.get(todo_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Todo not found")

    return {"error": "Todo not found"}


@app.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo: TodoCreate, todo_id: Annotated[int, Path(ge=1)]):
    if todo_id not in todo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Todo not found")
    todo_db[todo_id] = todo
    response = {"id": todo_id, **todo.model_dump()}

    return response

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: Annotated[int, Path(ge=1)]):
    if todo_id not in todo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Todo not found")
    todo_db.pop(todo_id, None)

    return {"Delete Operation":"Success"}
