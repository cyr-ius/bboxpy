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

    async def async_set_wireless(self, radio_enable: bool, wps_enable: bool) -> Any:
        """Set wireless."""
        return await self.async_request(
            "wireless",
            "post",
            data={"radio.enable": int(radio_enable), "wps.enable": int(wps_enable)},
        )

    async def async_set_wireless_24(self, data: dict[str, Any]) -> Any:
        """Configure 2.4Ghz."""
        id = self._get_wireless_id("24")
        return await self.async_request(f"wireless/{id}", method="put", data=data)

    async def async_set_wireless_24_state(self, enable: bool) -> Any:
        """Turn on/off 2.4Ghz."""
        return await self.async_set_wireless_24(data={"enable": int(enable)})

    async def async_set_wireless_5(self, data: dict[str, Any]) -> Any:
        """Configure 5Ghz."""
        id = self._get_wireless_id("5")
        return await self.async_request(f"wireless/{id}", method="put", data=data)

    async def async_set_wireless_5_state(self, enable: bool) -> Any:
        """Turn on/off 5Ghz."""
        return await self.async_set_wireless_5(data={"enable": int(enable)})

    async def async_set_wireless_guest(self, data: dict[str, Any]) -> Any:
        """Configure Guest."""
        id = self._get_wireless_id("guest")
        return await self.async_request(f"wireless/{id}", method="put", data=data)

    async def async_set_wireless_guest_state(self, enable: bool) -> Any:
        """Turn on/off Guest."""
        return await self.async_set_wireless_guest(data={"enable": int(enable)})

    async def _get_wireless_id(self, mode: str) -> Any:
        """Return wireless id."""
        wireless = await self.async_request("wireless")
        return wireless.get("ssid", {}).get(mode, {}).get("id")
