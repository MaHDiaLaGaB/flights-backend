from pydantic import BaseConfig
from datetime import datetime
from typing import Union


class FlightBase(BaseConfig):
    from_city: str
    to_city: str


class FlightSearch(FlightBase):
    date: datetime
    adults: int
    one_way: bool | False


