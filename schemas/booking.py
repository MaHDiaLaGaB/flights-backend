from schemas import ApiBase
from datetime import datetime
from typing import Union


class FlightBase(ApiBase):
    from_city: str
    to_city: str
    date: datetime


class FlightSearch(FlightBase):
    adults: int
    one_way: bool | False


