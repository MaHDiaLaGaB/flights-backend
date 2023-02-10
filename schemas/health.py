from schemas import ApiBase


class Health(ApiBase):
    status: str
    description: str
