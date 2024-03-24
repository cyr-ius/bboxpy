"""Provides authentication and raw access to Bouygues Bbox."""

from .bbox import Bbox
from .exceptions import (
    AuthorizationError,
    BboxException,
    HttpRequestError,
    ServiceNotFoundError,
    TimeoutExceededError,
)

__all__ = [
    "Bbox",
    "BboxException",
    "AuthorizationError",
    "TimeoutExceededError",
    "HttpRequestError",
    "ServiceNotFoundError",
]
