from fastapi import APIRouter, status, Depends, Body, HTTPException
from typing import Any, List, Dict
from .routes import SEARCH, CITY
from schemas import FlightBase, FlightResponse

import logging
from services.booking_service import Flights

route = APIRouter(tags=["booking"])


@route.post(CITY, status_code=status.HTTP_201_CREATED)
def search_city(*, flights: Flights = Depends(), city_nam: str) -> Any:
    res = flights.city_search(city_nam)
    return res


@route.post(SEARCH)
def get_flights(
    *, fly: FlightBase = Body(), flights: Flights = Depends()
) -> Dict[str, List[List[FlightResponse]]]:
    all_flights = dict()

    def get_all_flights(data: Any) -> List[List[FlightResponse]]:
        flights_group = []
        for offer in data:
            for itineraries in offer["itineraries"]:
                one_way_flights = []
                for segment in itineraries["segments"]:
                    one_way_flights.append(
                        FlightResponse(
                            id=int(offer["id"]),
                            departure=segment["departure"]["iataCode"],
                            arrival=segment["arrival"]["iataCode"],
                            airline=segment["carrierCode"],
                            flight_number=segment["number"],
                            departure_time=segment["departure"]["at"],
                            arrival_time=segment["arrival"]["at"],
                            duration=segment["duration"],
                            price=float(offer["price"]["grandTotal"]),
                        )
                    )
                flights_group.append(one_way_flights)
        return flights_group[:10]

    response = flights.flight_search(fly)
    all_flights["departure"] = get_all_flights(response)
    if not fly.one_way:
        if fly.return_date:
            if fly.return_date < fly.departure_date:
                logging.error("return date need to be after departure date")
                raise HTTPException(
                    detail="return date need to be after departure date",
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )
            fly.departure_date = fly.return_date
            _from, _to = fly.to_city, fly.from_city
            fly.from_city, fly.to_city = _from, _to
            resp = flights.flight_search(fly)
            return_flights = get_all_flights(resp)
            all_flights["return"] = return_flights
        else:
            logging.error("return date is missing")
            raise HTTPException(
                detail="return date is missing",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

    return all_flights
