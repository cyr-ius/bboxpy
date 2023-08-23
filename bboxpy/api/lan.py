"""Lan."""
from __future__ import annotations


class Lan:
    """Lan information."""

    def __init__(self, request):
        """Initialize."""
        self.async_request = request

    async def async_get_connected_devices(self):
        """Fetch data information."""
        return await self.async_request("GET", "v1/hosts")

    async def async_get_ip_infos(self):
        """Fetch data information."""
        return await self.async_request("GET", "v1/lan/ip")

    async def async_get_lan_stats(self):
        """Fetch data information."""
        return await self.async_request("GET", "v1/lan/stats")

    async def async_get_device_infos(self):
        """Fetch data information."""
        return await self.async_request("GET", "v1/hosts/me")
