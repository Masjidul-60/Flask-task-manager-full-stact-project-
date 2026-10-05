import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def test_health(client):
    assert client.get("/api/health").get_json() == {"status": "ok"}


def test_index_page(client):
    assert client.get("/").status_code == 200


def test_crud_flow(client):
    r = client.post("/api/tasks", json={"title": "Learn Flask"})
    assert r.status_code == 201
    task_id = r.get_json()["id"]

    assert len(client.get("/api/tasks").get_json()) == 1

    r = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert r.get_json()["done"] is True

    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get("/api/tasks").get_json() == []


def test_validation_and_404(client):
    assert client.post("/api/tasks", json={"title": "  "}).status_code == 400
    assert client.patch("/api/tasks/999", json={"done": True}).status_code == 404
    assert client.delete("/api/tasks/999").status_code == 404
