"""Dynamic DNS."""
from __future__ import annotations


class Ddns:
    """Dynamic DNS information."""

    def __init__(self, request):
        """Initialize."""
        self.async_request = request

    async def async_get_ddns(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/dyndns")

    async def async_get_ddns_by_id(self, by_id: int):
        """Fetch data information."""
        return await self.async_request("get", f"v1/dyndns/{by_id}")
