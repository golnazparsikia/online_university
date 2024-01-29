from enum import StrEnum


class OTPMsg(StrEnum):
    TOKEN_LENGTH = "`token_length` must be between `4` and `13` but actual length is `{token_length}`"

class TOTPMsg(StrEnum):
    LIFESPAN = "`lifespan` must be greater than and equal to `1` but actual lifespan is `{lifespan}`"


class HOTPMsg(StrEnum):
    pass
