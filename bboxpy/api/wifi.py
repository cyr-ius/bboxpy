"""Wifi."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal


class Wifi:
    """Wifi information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_wireless(self) -> Any:
        """Fetch data information."""
        return await self.async_request("wireless")

    async def async_get_stats_5(self) -> Any:
        """Fetch data information for 5Ghz."""
        return await self.async_request("wireless/5/stats")

    async def async_get_stats_24(self) -> Any:
        """Fetch data information for 2.4Ghz."""
        return await self.async_request("wireless/24/stats")

    async def async_get_wps(self) -> Any:
        """Fetch WPS information."""
        return await self.async_request("wireless/wps")

    async def async_on_wps(self) -> Any:
        """Enable WPS Session."""
        return await self.async_request("wireless/wps", "post")

    async def async_off_wps(self) -> Any:
        """Disable WPS Session."""
        return await self.async_request("wireless/wps", "delete")

    async def async_get_repeater(self) -> Any:
        """Fetch Repeater information."""
        return await self.async_request("wireless/repeater")

    async def async_set_wireless(self, enable: bool) -> Any:
        """Turn on/off all wireless interfaces."""
        return await self._async_set_wireless(state=enable)

    async def async_set_wireless_24(self, enable: bool) -> Any:
        """Turn on/off 2.4Ghz."""
        return await self._async_set_wireless(24, enable)

    async def async_set_wireless_5(self, enable: bool) -> Any:
        """Turn on/off 5Ghz."""
        return await self._async_set_wireless(5, enable)

    async def async_set_wireless_guest(self, enable: bool) -> Any:
        """Configure Guest."""
        return await self._async_set_wireless("guestenable", enable)

    async def _async_get_wireless_id(self, mode: str) -> Any:
        """Return wireless id."""
        wireless = await self.async_request("wireless")
        return wireless.get("ssid", {}).get(mode, {}).get("id")

    async def _async_set_wireless(
        self, wifi_id: Literal[24, 5, "guestenable"] | None = None, state: bool = True
    ) -> None:
        """Turn on wireless."""
        if wifi_id:
            return await self.async_request(
                f"wireless/{wifi_id}", method="put", params={"radio.enable": int(state)}
            )
        return await self.async_request(
            "wireless", method="put", params={"radio.enable": int(state)}
        )
