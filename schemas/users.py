from schemas import ApiBase


class UserBase(ApiBase):
    email: str
    username: str


class User(UserBase):
    is_active: bool
