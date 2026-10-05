from flask import Blueprint, jsonify, render_template, request
from .db import get_db

bp = Blueprint("main", __name__)


def row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "created_at": row["created_at"],
    }


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/api/health")
def health():
    return jsonify(status="ok")


@bp.get("/api/tasks")
def list_tasks():
    rows = get_db().execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@bp.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="title is required"), 400
    db = get_db()
    cur = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201


@bp.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return jsonify(error="not found"), 404
    title = (data.get("title", row["title"]) or "").strip() or row["title"]
    done = int(bool(data.get("done", row["done"])))
    db.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, task_id))
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return jsonify(row_to_dict(row))


@bp.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify(error="not found"), 404
    return "", 204
