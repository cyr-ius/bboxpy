"""IPTV."""
from __future__ import annotations


class IPTv:
    """IP Tv information."""

    def __init__(self, request):
        """Initialize."""
        self.async_request = request

    async def async_get_iptv_info(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/iptv")