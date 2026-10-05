# PyFullStack

A full-stack Python project: **Flask REST API + SQLite + HTML/CSS/JS frontend** (task manager), with tests, Docker and GitHub Actions CI.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
Open http://127.0.0.1:5000

## Test
```bash
pytest
```

## Docker
```bash
docker build -t pyfullstack .
docker run -p 8000:8000 pyfullstack
```

## API
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Health check |
| GET | /api/tasks | List tasks |
| POST | /api/tasks | Create `{ "title": "..." }` |
| PATCH | /api/tasks/<id> | Update `title` / `done` |
| DELETE | /api/tasks/<id> | Delete |

## Structure
```
app/            Flask package (routes, db, templates, static)
tests/          pytest tests
run.py          entry point
Dockerfile      container build
.github/        CI workflow
```
