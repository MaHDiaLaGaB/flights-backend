# pylint: disable=W0602
from typing import Dict, Type

from .const import ExceptionCategory
from .exception import AppException

KNOWN_EXCEPTIONS: Dict[str, Type[AppException]] = {}


def register_exception(
    exception_type: Type[AppException],
) -> Type[AppException]:
    key = exception_type.error_code()
    global KNOWN_EXCEPTIONS
    if key in KNOWN_EXCEPTIONS:
        raise Exception(
            f"Duplicate Exception with code {key} registered. {KNOWN_EXCEPTIONS[key]} and {exception_type}"
        )
    if exception_type.category_code not in [item.value for item in ExceptionCategory]:
        raise Exception(f"Unknown Category {exception_type.category_code}")
    KNOWN_EXCEPTIONS[key] = exception_type
    return exception_type
