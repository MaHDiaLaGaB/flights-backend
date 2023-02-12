from clients.amadues_client import AmadeusClient
from fastapi import HTTPException
from http import HTTPStatus
from schemas import FlightBase, ListOfAirPorts, CityName
from amadeus import ResponseError


class Flights:
    def __init__(self):
        self.amc = AmadeusClient()

    def flight_search(self, flight: FlightBase):
        try:
            resp = self.amc.amadeus.shopping.flight_offers_search.get(originLocationCode=flight.from_city,
                                                                      destinationLocationCode=flight.to_city,
                                                                      departureDate=flight.departure_date,
                                                                      adults=flight.adults)
            return resp.data
        except ResponseError as e:
            raise HTTPException(detail=e, status_code=HTTPStatus.BAD_REQUEST)

    def city_search(self, city_name: CityName):
        try:
            resp = self.amc.amadeus.reference_data.locations.cities.get(keyword=city_name)
            return resp.data

        except ResponseError as e:
            raise HTTPException(detail=e, status_code=HTTPStatus.BAD_REQUEST)
