#
# Base configuration for all envs
#


class BaseConfig:
    SENTRY_DSN: str = ""
    NAME: str = ""
    ENV: str = "dev_local"
    API_PORT: int = 0
