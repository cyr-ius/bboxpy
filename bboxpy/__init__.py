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
    "AuthorizationError",
    "Bbox",
    "BboxException",
    "HttpRequestError",
    "ServiceNotFoundError",
    "TimeoutExceededError",
]
