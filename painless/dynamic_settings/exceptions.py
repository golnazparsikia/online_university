from ..utils.exc import SerializableException

class SettingsNotAllowed(SerializableException):
    """
    Exception raised when a setting value cannot be set.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.args = (message,)

    def __str__(self) -> str:
        return self.args[0]

class InvalidEnvModeError(SerializableException):
    """
    Custom exception raised when an invalid environment mode is provided.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.args = (message,)

    def __str__(self) -> str:
        return self.args[0]
