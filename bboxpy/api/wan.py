"""Wan."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Wan:
    """Wan information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_wan_cpl(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/cpl")

    async def async_get_wan_cable(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/cable")

    async def async_get_wan_ftth(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/ftth/stats")

    async def async_get_wan_diags(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/diags")

    async def async_get_wan_ip(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/ip")

    async def async_get_wan_ip_stats(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/ip/stats")

    async def async_get_wan_xdsl(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/xdsl")

    async def async_get_wan_xdsl_stats(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/xdsl/stats")
