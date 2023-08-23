"""VOIP."""
from __future__ import annotations


class VOIP:
    """VOIP information."""

    def __init__(self, request):
        """Initialize."""
        self.async_request = request

    async def async_get_voip_voicemail(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/voip/voicemail")

    async def async_get_voip_callforward(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/voip/callforward")

    async def async_del_voip_calllog_by_id(self, by_id: int):
        """Fetch data information."""
        return await self.async_request("delete", f"v1/voip/calllog/{by_id}")
