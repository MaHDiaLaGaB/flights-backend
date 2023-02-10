from http import HTTPStatus
from typing import Any, Dict, Optional, Union

from .const import ExceptionCategory


class AppException(Exception):
    category_code: int = ExceptionCategory.GENERIC
    exception_code: int = 1
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    description: Optional[str] = "Internal Server Error"
    payload: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        description: Union[str, Any] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__()
        self.description = description or self.description
        self.payload = payload

    @classmethod
    def error_code(cls) -> str:
        return f"E{cls.category_code:03}{cls.exception_code:03}"
