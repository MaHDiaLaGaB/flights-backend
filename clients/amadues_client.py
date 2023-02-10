from amadeus import Client
from amadeus.client.errors import AuthenticationError
from config import Config
import logging

logger = logging.getLogger('your_logger')
logger.setLevel(logging.DEBUG)


class AmadeusClient:
    def __init__(self):
        try:
            logger.info("Initialize Amadeus Client with credentials")
            self.amadeus = Client(client_id=Config.AMADEUS_API_KEY,
                                  client_secret=Config.AMADEUS_API_SECRETS,
                                  logger=logger)
        except AuthenticationError as e:
            raise f"Please check Clients credentials: {e}"
