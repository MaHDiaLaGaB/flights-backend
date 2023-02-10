from api.routes import HEALTH
from http import HTTPStatus
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    resp = client.get(HEALTH)
    assert resp.status_code == HTTPStatus.OK
