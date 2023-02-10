from fastapi import HTTPException, APIRouter, status
from db.database import DB
from exceptions import NotFound
from schemas import User, UserBase

from .routes import CREATE_USER, USER

route = APIRouter(tags=["users"])

db = DB()


@route.post(CREATE_USER, response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(*, user: UserBase) -> User:
    db_user = db.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db.create_user(user=user)


@route.get(USER, response_model=User)
def read_users(*, user_id: int) -> User:
    db_user = db.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="user not in database")
    return db_user


@route.delete(USER, response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(*, user_id: int, user_email: str):
    db_user = db.get_user_by_id(user_id)
    if db_user is None:
        raise NotFound(description="no user")
    db.delete_user_by_email(email=user_email, user_id=user_id)
