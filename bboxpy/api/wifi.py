"""Wifi."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Wifi:
    """Wifi information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_wireless(self) -> Any:
        """Fetch data information."""
        return await self.async_request("wireless")

    async def async_get_stats_5(self) -> Any:
        """Fetch data information."""
        return await self.async_request("wireless/5/stats")

    async def async_get_stats_24(self) -> Any:
        """Fetch data information."""
        return await self.async_request("wireless/24/stats")

    async def async_get_wps(self) -> Any:
        """Fetch data information."""
        return await self.async_request("wireless/wps")

    async def async_on_wps(self) -> Any:
        """Fetch data information."""
        return await self.async_request("wireless/wps", "post")

    async def async_off_wps(self) -> Any:
        """Fetch data information."""
        return await self.async_request("wireless/wps", "delete")

    async def async_get_repeater(self) -> Any:
        """Fetch data information."""
        return await self.async_request("wireless/repeater")

    async def async_set_wireless(self, enable: bool) -> Any:
        """Fetch data information."""
        return await self.async_request(
            "wireless", "post", data={"enable": int(enable)}
        )
