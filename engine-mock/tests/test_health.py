from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# TODO(Person 1): add tests for each endpoint as you build it, e.g.
# - transfer_into_space returns 400 when the balance is too low
# - next_month runs a due standing order exactly once
