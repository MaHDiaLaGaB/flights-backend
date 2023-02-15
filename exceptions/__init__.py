from http import HTTPStatus
from .registry import register_exception
from .exception import AppException
from .const import ExceptionCategory
from typing import Optional
from typing import Union


@register_exception
class GenericHTTPException(AppException):
    category_code: int = ExceptionCategory.ENTITY
    exception_code: int = 100
    status_code: int = HTTPStatus.NOT_FOUND
    description: Optional[str] = "Http Exception"

    def __init__(self, status_code: int = HTTPStatus.NOT_FOUND) -> None:
        super().__init__()
        self.status_code = status_code


@register_exception
class NotFound(AppException):
    category_code: int = ExceptionCategory.GENERIC
    exception_code: int = 2
    status_code: int = HTTPStatus.NOT_FOUND
    description: Optional[str] = "Requested object not found"

    def __init__(self, object_id: Optional[str] = None) -> None:
        super().__init__()
        if object_id:
            self.description: Optional[str] = f"Object with id {object_id} not found"


@register_exception
class ObjectNotFound(AppException):
    category_code: int = ExceptionCategory.ENTITY
    exception_code: int = 1
    status_code: int = HTTPStatus.NOT_FOUND
    description: Optional[str] = "Requested object not found"

    def __init__(self, object_id: Union[str, int] | None) -> None:
        super().__init__()
        if object_id:
            self.description: Optional[
                str
            ] = f"Requested object with id '{object_id}' not found"


@register_exception
class DocumentRendererServiceException(AppException):
    category_code: int = ExceptionCategory.DOCUMENT_RENDERER_SERVICE
    exception_code: int = 1


@register_exception
class DocumentProcessorServiceException(DocumentRendererServiceException):
    exception_code: int = 2
