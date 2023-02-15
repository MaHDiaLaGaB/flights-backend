from pytest import fixture
from server import app

from fastapi.testclient import TestClient


@fixture
def client() -> TestClient:
    return TestClient(app)


placeholders = {"name": "mahdi", "age": "24,"}
