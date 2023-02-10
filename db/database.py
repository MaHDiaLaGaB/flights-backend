from typing import Generator, Type, cast, TypeVar
import logging
from sqlalchemy import create_engine
from .models import Base, User
from sqlalchemy.orm import sessionmaker, Session
from exceptions import ObjectNotFound
from sqlalchemy import func
from schemas import UserBase
from config import Config

T = TypeVar("T", bound=UserBase)


class DB:
    def __init__(self) -> None:
        self._engine = create_engine(
            Config.SQLALCHEMY_DATABASE_DEV_URI,
            connect_args={"check_same_thread": False},
        )
        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )
        self.db_session: Session = self._session_factory()
        self._engine.connect()

    def session(self) -> Generator[int, None, None]:
        try:
            yield self.db_session  # type: ignore
        except Exception:
            logging.exception("session rollback")
            self.db_session.rollback()
            raise
        finally:
            self.db_session.close()

    def drop_tables(self) -> None:
        Base.metadata.drop_all(bind=self._engine, checkfirst=True)

    def create_tables(self) -> None:
        Base.metadata.create_all(self._engine)

    def reset(self) -> None:
        self.drop_tables()
        self.create_tables()

    def add_email(self, email: str) -> None:
        if not self.db_session:
            raise Exception("Database not initialized")

        self.db_session.add(email)
        self.db_session.commit()

    def create_user(self, user: UserBase) -> User:
        if not self.db_session:
            raise Exception("Database not initialized")
        db_user = self.get_user_by_email(user.email)
        if db_user:
            raise Exception("user is already signup")
        db_user = User(email=user.email, username=user.username)
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        return db_user

    # i will keep the ID int for now until i store the id by type uuid
    def _get_by_id(self, model: Type[T], entity_id: int) -> T:
        entity = self.db_session.query(model).get(entity_id)
        if not entity:
            raise ObjectNotFound(str(entity_id))
        return cast(T, entity)

    def get_user_by_email(self, email: str) -> User:
        if not self.db_session:
            raise Exception("Database not initialized")
        user = (
            self.db_session.query(User)
            .filter((func.lower(User.email == email.lower())))
            .first()
        )
        return cast(User, user)

    def get_user_by_id(self, user_id: int) -> User:
        return self._get_by_id(User, user_id)

    def delete_user_by_email(self, email: str, user_id: int) -> None:
        if not self.db_session:
            raise Exception("Database not initialized")

        user = self.get_user_by_id(user_id)
        if user.email != email:
            raise ObjectNotFound()

        self.db_session.query(User).filter(
            (func.lower(User.email == email.lower()))
        ).delete()
