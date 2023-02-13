from clients.amadues_client import AmadeusClient
from schemas import FlightBase
from amadeus import ResponseError, Location


class Flights:
    def __init__(self):
        self.amc = AmadeusClient()

    def flight_search(self, flight: FlightBase):

        try:
            resp = self.amc.amadeus.shopping.flight_offers_search.get(originLocationCode=flight.from_city,
                                                                      destinationLocationCode=flight.to_city,
                                                                      departureDate=flight.departure_date,
                                                                      adults=flight.adults)

            #  return the first four flights
            return resp.data[:4]
        except ResponseError as error:
            raise error

    def city_search(self, city_name: str):
        city_name = city_name.title()
        try:
            resp = self.amc.amadeus.reference_data.locations.get(keyword=city_name, subType=Location.ANY)

            return resp.data

        except ResponseError as error:
            raise error
