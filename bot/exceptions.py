"""Custom exceptions for the trading bot."""


class ValidationError(Exception):
    """Raised when user input fails validation."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class APIError(Exception):
    """Raised when Binance rejects a request."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NetworkError(Exception):
    """Raised on connection/timeout failures."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ConfigurationError(Exception):
    """Raised when required env vars are missing."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
