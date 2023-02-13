from fastapi import APIRouter, status, Depends, Body
from typing import Any
from .routes import SEARCH, CITY
from schemas import FlightBase
import logging
from services.booking_repo import Flights

route = APIRouter(tags=["booking"])


@route.post(SEARCH, status_code=status.HTTP_201_CREATED)
def search_flight(*, flights: Flights = Depends(), fly: FlightBase = Body()) -> Any:
    logging.info(f"searching for flights from {fly.from_city} to {fly.to_city}")
    res = flights.flight_search(flight=fly)
    return res


@route.post(CITY, status_code=status.HTTP_201_CREATED)
def search_city(*, flights: Flights = Depends(), city_nam: str) -> Any:
    res = flights.city_search(city_nam)
    return res
