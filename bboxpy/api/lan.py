"""Lan."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Lan:
    """Lan information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_connected_devices(self) -> Any:
        """Fetch data information."""
        return await self.async_request("hosts")

    async def async_get_ip_infos(self) -> Any:
        """Fetch data information."""
        return await self.async_request("lan/ip")

    async def async_get_lan_stats(self) -> Any:
        """Fetch data information."""
        return await self.async_request("lan/stats")

    async def async_get_device_infos(self) -> Any:
        """Fetch data information."""
        return await self.async_request("hosts/me")
