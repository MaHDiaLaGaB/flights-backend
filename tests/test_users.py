from api.routes import CREATE_USER, USER
from http import HTTPStatus
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from db.models import User
from db.database import DB

user = {"email": "john_doe@test.com", "username": "john doe"}


def test_create_user(client: TestClient, user_1: User, database: DB) -> None:
    resp = client.post(CREATE_USER, json=user)
    assert resp.status_code == HTTPStatus.CREATED
    get_user = database.get_user_by_email(user_1["email"])
    assert get_user.__str__() == user["email"]


def test_delete_user(client: TestClient, database: DB, user_2: User):
    pass
