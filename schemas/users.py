from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str

    class Config:
        orm_mode = True


class User(UserBase):
    is_active: bool

    class Config:
        orm_mode = True
