"""Services."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Services:
    """Services information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_bbox_services(self) -> Any:
        """Fetch data information."""
        return await self.async_request("services")

    async def async_get_events_notification_service(self) -> Any:
        """Fetch data information."""
        return await self.async_request("notification")
