"""
You can add categories as much as you can
"""
from enum import IntEnum


class ExceptionCategory(IntEnum):
    # generic
    GENERIC = 1

    # exceptions related to the endpoints
    ENTITY = 100

    # users
    USERS = 200

    # Clients
    ...

    # Services
    DOCUMENT_RENDERER_SERVICE = 300
