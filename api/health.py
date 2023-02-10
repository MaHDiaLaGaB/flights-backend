from fastapi import APIRouter
from api import routes
from schemas import Health

route = APIRouter(tags=["health"])


@route.get(routes.HEALTH, response_model=Health)
def health_check() -> Health:
    return Health(status="OK", description="The API is reachable")
