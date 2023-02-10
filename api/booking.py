from fastapi import APIRouter, HTTPException, status, Depends
from clients.amadues_client import AmadeusClient
from amadeus import ResponseError
from .routes import SEARCH


route = APIRouter(tags=["booking"])


@route.get(SEARCH, status_code=status.HTTP_200_OK)
def search_flight(*, amc: AmadeusClient = Depends(AmadeusClient)):
    try:
        resp = amc.amadeus.shopping.flight_offers_search.get(originLocationCode='MAD',
                                                             destinationLocationCode='ATH',
                                                             departureDate='2023-04-01',
                                                             adults=1)
        return resp.data
    except ResponseError as e:
        raise HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
