# API Design Spec: Todo API (Beginner)

## Step 1: Domain & Resource Modeling

### 1. Resource: `Todo`
* **What it represents:** [1-sentence description]

| Field         | Type          | Controlled By | Constraints / Defaults                                                |
|:--------------|:--------------|:--------------|:----------------------------------------------------------------------|
| `id`          | `int`         | **Server**    | Auto-increment, `>= 1`                                                |
| `title`       | `str`         | **Client**    | Required, `min_length=1`, `max_length=100`                            |
| `description` | `str \| None` | **Client**    | Optional, default `None`, `max_length=500`                            |
| `done`        | `bool`        | **Both**      | Server defaults to `False` on create; Client can update via PUT/PATCH |
| `created_at`  | `datetime`    | **Server**    | Auto-set to current UTC timestamp on creation                         |

### 2. Business Rules & Invariants (What can NEVER happen?)
* Rule 1: A title cannot be empty or just spaces.
* Rule 2: A client cannot manually set or change `id` or `created_at`.
* Rule 3: Requesting, updating, or deleting a non-existent `id` must immediately fail with a 404.

---

## Step 2: API Contract Matrix

### 1. Endpoints

| Action           | Method & Path        | Query Params                                    | Request Body  | Happy Status & Response       | Failure Modes (Status)                               |
|:-----------------|:---------------------|:------------------------------------------------|:--------------|:------------------------------|:-----------------------------------------------------|
| **Create**       | `POST /todos`        | —                                               | `TodoCreate`  | `201 Created` → `TodoPublic`  | `422` (Invalid/missing fields)                       |
| **List All**     | `GET /todos`         | `done: bool \| None`<br>`sort: "asc" \| "desc"` | —             | `200 OK` → `list[TodoPublic]` | `422` (Bad query type)                               |
| **Get One**      | `GET /todos/{id}`    | —                                               | —             | `200 OK` → `TodoPublic`       | `404` (Not found)<br>`422` (`id < 1` or not an int)  |
| **Replace**      | `PUT /todos/{id}`    | —                                               | `TodoReplace` | `200 OK` → `TodoPublic`       | `404` (Not found)<br>`422` (Missing required fields) |
| **Partial Edit** | `PATCH /todos/{id}`  | —                                               | `TodoPatch`   | `200 OK` → `TodoPublic`       | `404` (Not found)<br>`422` (Invalid field types)     |
| **Delete**       | `DELETE /todos/{id}` | —                                               | —             | `204 No Content` → `None`     | `404` (Not found)                                    |

### 2. Schema Mapping Checklist (To build in `schemas.py` next)
* [x] **`[Resource]Create`** (Input for `POST`): Only fields marked **Client** above.
* [ ] **`[Resource]Replace`** (Input for `PUT`): All mutable **Client/Both** fields required.
* [ ] **`[Resource]Patch`** (Input for `PATCH`): All mutable **Client/Both** fields set to `Optional` with default `None`.
* [ ] **`[Resource]Public`** (Output for responses): All fields (**Client** + **Server**).