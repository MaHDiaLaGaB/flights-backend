import logging

from clients.amadues_client import AmadeusClient
from schemas import FlightBase
from amadeus import ResponseError, Location
from typing import Any
from utils.doc_utils import find_by_city_name, find_by_airport_name


class Flights:
    def __init__(self) -> None:
        self.amc = AmadeusClient()

    def flight_search(self, flight: FlightBase) -> Any:
        try:
            flight.from_city = find_by_city_name(flight.from_city)
            flight.to_city = find_by_city_name(flight.to_city)
            params = {
                "originLocationCode": flight.from_city,
                "destinationLocationCode": flight.to_city,
                "departureDate": flight.departure_date,
                "adults": flight.adults,
            }
            logging.info("searching for flights ...")
            resp = self.amc.amadeus.shopping.flight_offers_search.get(**params)

            #  return the first four flights
            return resp.data
        except ResponseError as error:
            raise error

    def city_search(self, city_name: str) -> Any:
        city_name = city_name.title()
        logging.info("searching for cities ...")
        try:
            resp = self.amc.amadeus.reference_data.locations.get(
                keyword=city_name, subType=Location.ANY
            )

            return resp.data

        except ResponseError as error:
            raise error
