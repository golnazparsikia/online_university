
class TokenError(Exception):

    def __init__(self, message="Token Error"):
        self.message = message
        super().__init__(self.message)


class TokenLengthError(ValueError):

    def __init__(self, message="`token_length` must be between 4 and 13"):
        self.message = message
        super().__init__(self.message)


class TokenLifeSpanError(ValueError):

    def __init__(self, message="Token Lifespan must be Positive."):
        self.message = message
        super().__init__(self.message)
