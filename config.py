from dotenv import load_dotenv
from configuration.base_configuration import BaseConfig
from configuration import generate_config
from typing import cast


class Config(BaseConfig):
    NAME = "mocks"
    API_PORT = 7500
    SQLALCHEMY_DATABASE_DEV_URI: str = "sqlite:///flightsDB.db"
    AMADEUS_API_KEY: str = ""
    AMADEUS_API_SECRETS: str = ""


load_dotenv()

config = cast(Config, generate_config(Config))  # pylint: disable=C0103
config.API_PORT = int(config.API_PORT)
config.AMADEUS_API_KEY = str(config.AMADEUS_API_KEY)
config.AMADEUS_API_SECRETS = str(config.AMADEUS_API_SECRETS)
