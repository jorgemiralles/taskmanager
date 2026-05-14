# AGENTS.md — Task Manager

Simple Flask task manager with MySQL backend and Bootstrap 5 frontend.
Single-page CRUD app with priority levels, due dates, and completion toggling.
Created by OpenCode (big-pickle model). Language: Python / JavaScript / SQL.

## Quick start

```sh
# Install mysql client if needed (Alpine: apk add mariadb-client)
source venv/bin/activate
mysql -h "$DB_HOST" -u root -proot --ssl=0 < schema.sql
python app.py          # http://0.0.0.0:5000
```

## Architecture

- **Backend**: Single Flask app (`app.py`) with 5 REST endpoints under `/api/tasks`
  - `GET` — list all tasks (ordered by `created_at DESC`)
  - `POST` — create task (title, priority, due_date)
  - `PUT /<id>` — update task fields
  - `PATCH /<id>/toggle` — flip `completed` boolean
  - `DELETE /<id>` — remove task
- **Frontend**: Single HTML page (`templates/index.html`) with vanilla JS, Bootstrap 5 CDN, Bootstrap Icons. No build step.
- **DB**: MySQL with `ENUM('low','medium','high')` priority, `DATE` due_date, `BOOLEAN` completed, `TIMESTAMP` created_at
- **Data flow**: frontend fetches JSON from `/api/tasks`, renders task cards, attaches inline edit/delete/toggle handlers. No page reloads.

## Project structure

- `app.py` — single Flask entrypoint with all routes
- `templates/index.html` — single-page frontend (Bootstrap 5 + vanilla JS)
- `schema.sql` — runs `CREATE DATABASE` + `CREATE TABLE tasks`
- `.env` — `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (gitignored)
- `tests/` — pytest integration tests (uses isolated `taskmanager_test` database)

## Git practices

- Use [Conventional Commits] format: `<type>[optional scope]: <description>`
  - Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `style`, `test`, `perf`, `build`, `ci`
  - Add `!` after type/scope for breaking changes
  - Optional body (blank line after description) and footers (e.g. `BREAKING CHANGE:`)
- Keep commits focused on a single change

## Python conventions

- Use `mysql.connector` directly — no ORM. Raw SQL with `%s` placeholders.
- DB connection via `get_db()` helper in `app.py` — returns a new connection each call.
- Flask app uses `@app.route()` decorators, global `app` object, `jsonify` for API responses.
- `.env` is NOT auto-loaded (no `python-dotenv` installed). Export vars or source `.env` before running.
- All API routes return JSON — no server-side templates except the root `/` serving `index.html`.

## Coding style

- No comments, no docstrings — code should be self-explanatory.
- No type hints — keep it simple.
- Single quotes for strings.
- snake_case for functions and variables.
- No linter/formatter config enforced — match existing style.

## Key facts

- Integration tests in `tests/` — run with `pytest` from project root (requires MySQL). Uses isolated `taskmanager_test` DB.
- No linter/formatter/typecheck config. Nothing else to run before commit.
- DB credentials are hardcoded in `.env` — never commit `.env`.
- venv uses Python 3.12 with `flask` and `mysql-connector-python`.
- MySQL host `mimysql` suggests a Docker/container network — verify connectivity if running elsewhere.