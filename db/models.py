from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, String, Integer, Column
from typing import Any

Base: Any = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    is_active = Column(Boolean, default=True)

    def __str__(self) -> str:
        return str(self.email)
