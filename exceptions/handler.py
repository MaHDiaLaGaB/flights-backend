import logging
import traceback
from typing import Any, Dict, cast

from fastapi.responses import JSONResponse

from configuration.base_configuration import BaseConfig
from reporting import report_exception

from .exception import AppException
from .registry import KNOWN_EXCEPTIONS


def handle_exception(config: BaseConfig, exception: Exception) -> JSONResponse:
    report_exception(exception)

    # try to handle one of our exceptions
    if issubclass(exception.__class__, AppException):
        App_exception = cast(AppException, exception)
        error_code = App_exception.error_code()

        if error_code not in KNOWN_EXCEPTIONS:
            raise Exception("Tried to use unregistered exception")

        response: Dict[str, Any] = {
            "error_code": error_code,
            "description": App_exception.description,
        }

        if hasattr(App_exception, "payload"):
            response["payload"] = App_exception.payload

        status_code = App_exception.status_code
    else:
        # default is 500
        response = {
            "error_code": AppException.error_code(),
            "description": AppException.description,
        }
        status_code = AppException.status_code

    # when developing locally print stacktrace to output
    if config.ENV == "dev_local":
        logging.info(traceback.format_exc())

    # on all dev envs send stacktrace in response
    if "dev" in config.ENV:
        response["stacktrace"] = traceback.format_exc()

    return JSONResponse(
        status_code=status_code,
        content=response,
    )
