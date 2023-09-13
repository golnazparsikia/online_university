from enum import StrEnum, auto
from typing import Optional
from .exceptions import InvalidEnvModeError


class EnvMode(StrEnum):
    DEVELOPMENT =   'dev'
    STAGE       =   'stage'
    PRODUCTION  =   'prod'

    @classmethod
    def validate(cls, mode: str, raise_exception: bool = False) -> bool:
        is_validated = True
        if mode not in tuple(cls):
            if raise_exception:
                raise InvalidEnvModeError(
                    f"Invalid environment mode '{mode}'."
                    f"Must be one of {list(cls)}"
                )
            else:
                is_validated = False
        return is_validated
