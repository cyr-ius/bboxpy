"""Exceptions for BBox."""


class BboxException(Exception):
    """General exception."""


class AuthorizationError(BboxException):
    """Authentification error."""


class HttpRequestError(BboxException):
    """HTTP Requests error."""


class TimeoutExceededError(BboxException):
    """Timeout exceeded."""


class ServiceNotFoundError(BboxException):
    """Service not found."""
