from pytest import fixture
from server import app
from typing import Generator, Any, Dict
from fastapi.testclient import TestClient
from db.database import DB
from sqlalchemy.orm import Session

db = DB()


@fixture
def client() -> TestClient:
    return TestClient(app)


@fixture
def database() -> Generator[Any, Any, Any]:
    yield db


@fixture(autouse=True)
def run_around_tests():  # type: ignore
    db.reset()
    yield db.reset()  # type: ignore


@fixture(autouse=True)
def database_session() -> Generator[Any, Any, Any]:
    yield db.db_session


@fixture
def user_1() -> Dict[str, Any]:
    return {"email": "john_doe@test.com", "username": "john doe"}


@fixture
def user_2() -> Dict[str, Any]:
    return {"email": "mad_jon@test.com", "username": "mahdi doe"}
