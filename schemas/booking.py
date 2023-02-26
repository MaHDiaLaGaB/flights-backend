from .base import ApiBase
from typing import List, Optional, Dict
from pydantic import Field, root_validator, BaseModel


class FlightBase(BaseModel):
    from_city: str
    to_city: str
    departure_date: str
    return_date: Optional[str]
    adults: int
    one_way: bool

    @root_validator
    def set_return_date(cls, values: Dict[str, str]) -> Dict[str, str]:
        if not values["one_way"]:
            if "return_date" not in values or not values["return_date"]:
                raise ValueError("return_date is required for round-trip flights")
        return values


class FlightResponse(ApiBase):
    id: int
    departure: str
    arrival: str
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
