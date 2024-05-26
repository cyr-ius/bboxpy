"""Dynamic DNS."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Ddns:
    """Dynamic DNS information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_ddns(self) -> Any:
        """Fetch data information."""
        return await self.async_request("dyndns")

    async def async_get_ddns_by_id(self, by_id: int) -> Any:
        """Fetch data information."""
        return await self.async_request(f"dyndns/{by_id}")
