from fastapi import APIRouter, status, Depends, Body
from .routes import SEARCH
from schemas import FlightBase, ListOfAirPorts, CityName
from utils.booking_repo import Flights

route = APIRouter(tags=["booking"])


@route.post(SEARCH, status_code=status.HTTP_201_CREATED)
def search_flight(*, flights: Flights = Depends(), fly: FlightBase = Body()):
    res = flights.flight_search(flight=fly)
    return res


@route.post("/booking/city/", status_code=status.HTTP_201_CREATED, response_model=ListOfAirPorts)
def search_flight(*, flights: Flights = Depends(), city_name: CityName):
    res = flights.city_search(city_name)
    return res
