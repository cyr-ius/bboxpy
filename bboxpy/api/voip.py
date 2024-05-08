"""VOIP."""

from __future__ import annotations

from typing import Any, Callable


class VOIP:
    """VOIP information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_voip_voicemail(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/voip/voicemail")

    async def async_get_voip_callforward(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/voip/callforward")

    async def async_del_voip_calllog_by_id(self, by_id: int) -> None:
        """Fetch data information."""
        await self.async_request("delete", f"v1/voip/calllog/{by_id}")
