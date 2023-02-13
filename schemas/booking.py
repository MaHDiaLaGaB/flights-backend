from .base import ApiBase

from typing import Union, List


class FlightBase(ApiBase):
    from_city: str
    to_city: str
    departure_date: str
    adults: int


class FlightSearch(FlightBase):
    one_way: bool = False


class BookMock(FlightSearch):
    name: str
    passport: str


class CityName(ApiBase):
    city_name: str


class Address(ApiBase):
    countryCode: str
    stateCode: str


class GeoCode(ApiBase):
    latitude: float
    longitude: float


class CitysAirPorts(ApiBase):
    type: str
    subType: str
    name: str
    iataCode: str
    address: Union[Address, None]
    geo_address: Union[GeoCode, None]


#  TODO i need to fix this
class ListOfAirPorts(CitysAirPorts):
    list_of_ports: List[CitysAirPorts]
