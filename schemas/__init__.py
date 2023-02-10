from .health import Health
from .users import User, UserBase
from pydantic import BaseModel


class ApiBase(BaseModel):
    class Config:
        orm_mode = True
        extra = "forbid"
        use_enum_values = True
        anystr_strip_whitespace = True
        validate_all = True
        validate_assignment = True
        allow_inf_nan = False
