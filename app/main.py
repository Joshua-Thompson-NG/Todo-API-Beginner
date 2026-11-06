from datetime import UTC, datetime
from typing import Literal

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

# SCHEMA MODELS

# Input for POST
class TodoCreate(BaseModel):
    title: str = Field(...,min_length=1,max_length=100,
                        description="The title of the todo.",
                        examples=["Washing Dishes"])
    description: str | None = Field(default=None, max_length=500,
                                    description="Optional Detailed Description",
                                    examples=["Check If I have any dishes to wash today"])  # noqa: E501
    @field_validator("title",mode="before")
    @classmethod
    def strip_title(cls, value:object) -> object:
        return value.strip() if isinstance(value, str) else value

# Input for PUT
class TodoReplace(BaseModel):
    title: str = Field(...,min_length=1,max_length=100)
    description: str | None = Field(default=None, max_length=500)
    done: bool = Field(..., description="The status of a todo.")

    @field_validator("title", mode="before")
    @classmethod
    def strip_title(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

# Input for PATCH
class TodoPatch(BaseModel):
    title: str | None = Field(default=None,min_length=1,max_length=100)
    description: str | None = Field(default=None, max_length=500)
    done: bool | None = None

    @field_validator("title", mode="before")
    @classmethod
    def strip_title(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

# Output for responses
class TodoPublic(BaseModel):
    id: int
    title: str
    description: str | None
    done: bool
    created_at: datetime

# IN MEMORY DB
todo_db:dict[int,dict] = {}
current_id=1

# ENDPOINTS

@app.post("/todos", response_model=TodoPublic, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate):
    global current_id

    # Rule 1: title cannot be empty
    if not payload.title:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Title cannot be empty.")

    new_todo = {
        "id": current_id,
        "title": payload.title,
        "description": payload.description,
        "done": False,
        "created_at": datetime.now(UTC)
    }

    todo_db[current_id] = new_todo
    current_id += 1
    return new_todo


@app.get("/todos", response_model=list[TodoPublic], status_code=status.HTTP_200_OK)
def list_all_todos(
        done: bool | None = Query(None,
                                  description="Filter by status of todo."),
        sort: Literal["asc", "desc"] = Query("asc",
                                    description="Sort by ID chronological order.")
        ):

    todo_list = list(todo_db.values())

    if done is not None:
        todo_list = [todo for todo in todo_list if todo["done"] == done]

    reverse_sort = True if sort == "desc" else False
    todo_list.sort(key=lambda x: x["id"], reverse=reverse_sort)

    return todo_list


@app.get("/todos/{id}", response_model=TodoPublic, status_code=status.HTTP_200_OK)
def get_todo(id: int = Path(...,ge=1,
                            description="The ID of the todo item to retrieve")):
    if id not in todo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID not found")
    return todo_db[id]


@app.put("/todos/{id}", response_model=TodoPublic, status_code=status.HTTP_200_OK)
def replace_todo(payload: TodoReplace,
                 id: int = Path(...,
                 description="The ID of the todo item to replace completely")):
    if id not in todo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID not found"
        )

    existing_id = todo_db[id]

    update_todo = {
        "id":existing_id["id"],
        "title": payload.title,
        "description": payload.description,
        "done": payload.done,
        "created_at": existing_id["created_at"]
    }

    todo_db[id]= update_todo
    return update_todo

@app.patch("/todos/{id}", response_model=TodoPublic, status_code=status.HTTP_200_OK)
def partially_update(payload: TodoPatch,
                     id: int = Path(ge=1,
                description="The ID of the todo item to partially modify")):
    if id not in todo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID not found"
        )

    existing_id = todo_db[id]

    update_todo = payload.model_dump(exclude_unset=True)

    for key, value in update_todo.items():
        existing_id[key] = value

    return existing_id

@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id : int = Path(...,ge=1,
                            description="The ID of the todo item to delete")):
    if id not in todo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID not found"
        )

    del todo_db[id]
    return None

