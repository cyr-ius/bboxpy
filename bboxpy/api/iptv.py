"""IPTV."""

from __future__ import annotations

from typing import Any, Callable


class IPTv:
    """IP Tv information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_iptv_info(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/iptv")
