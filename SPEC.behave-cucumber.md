# Add Cucumber (behave) BDD Testing Framework

## Goal

Add Gherkin-based BDD acceptance tests using Python's `behave`
framework, alongside existing pytest integration tests.

---

## Plan

### 1. Files to modify

| File | Change |
|---|---|
| `requirements.txt` | Append `behave` |

### 2. Files to create

| File | Purpose |
|---|---|
| `features/tasks.feature` | Gherkin scenarios covering all 5 API endpoints |
| `features/environment.py` | Test DB lifecycle + Flask test client setup |
| `features/steps/__init__.py` | Package marker (empty) |
| `features/steps/task_steps.py` | Step definitions |
| `SPEC.behave-cucumber.md` | This document |

### 3. Architecture

```
features/
├── tasks.feature          ← Gherkin scenarios
├── environment.py         ← before_all / after_all / before_scenario
└── steps/
    ├── __init__.py
    └── task_steps.py      ← @given / @when / @then
```

### 4. DB lifecycle (environment.py)

- **before_all**: load `.env`, override `DB_NAME = taskmanager_test`, create DB + table, init Flask test client
- **after_all**: drop `taskmanager_test` database
- **before_scenario**: `TRUNCATE tasks` for clean slate

Reuses the same pattern as `tests/conftest.py`.

### 5. Gherkin scenarios (tasks.feature)

| # | Scenario | Endpoints exercised |
|---|---|---|
| 1 | View empty task list | GET |
| 2 | Create a task | POST |
| 3 | Create with priority and due date | POST, GET |
| 4 | List tasks after creation | POST ×2, GET |
| 5 | Update a task | POST, PUT, GET |
| 6 | Toggle task completion | POST, PATCH ×2, GET |
| 7 | Delete a task | POST, DELETE, GET |
| 8 | Full task lifecycle | POST, PATCH, PUT, DELETE, GET |

### 6. Step definitions (task_steps.py)

- Store `context.response` (last HTTP response) and `context.task_id` (last operated task ID)
- `context.client` is the Flask test client, set in `before_all`
- Use `behave`'s `@given`, `@when`, `@then` decorators with parse expressions
- Assert on response status codes and JSON body

### 7. Running

```sh
source venv/bin/activate && behave
```

Expected: 8 scenarios, all passing.

### 8. Non-goals

- No changes to `app.py`, `schema.sql`, or `tests/`
- No linter/formatter config
- `behave` is a dev dependency only
