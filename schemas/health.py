from .base import ApiBase


class Health(ApiBase):
    status: str
    description: str
