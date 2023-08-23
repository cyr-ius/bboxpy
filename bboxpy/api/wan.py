"""Wan."""
from __future__ import annotations


class Wan:
    """Wan information."""

    def __init__(self, request):
        """Initialize."""
        self.async_request = request

    async def async_get_wan_cpl(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/cpl")

    async def async_get_wan_cable(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/cable")

    async def async_get_wan_ftth(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/ftth/stats")

    async def async_get_wan_diags(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/diags")

    async def async_get_wan_ip(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/ip")

    async def async_get_wan_ip_stats(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/ip/stats")

    async def async_get_wan_xdsl(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/xdsl")

    async def async_get_wan_xdsl_stats(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/wan/xdsl/stats")
