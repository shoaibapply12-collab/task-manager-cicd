from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 420
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["done"] is False


def test_get_tasks_grows():
    before = client.get("/tasks").json()
    client.post("/tasks", json={"title": "Another task"})
    after = client.get("/tasks").json()

    assert isinstance(after, list)
    assert len(after) == len(before) + 1


def test_create_task_empty_title_fails():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400
