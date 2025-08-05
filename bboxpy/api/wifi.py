"""Wifi."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Wifi:
    """Wifi information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        self.async_request = request

    async def async_get_wireless(self) -> Any:
        return await self.async_request("wireless")

    async def async_get_stats_5(self) -> Any:
        return await self.async_request("wireless/5/stats")

    async def async_get_stats_24(self) -> Any:
        return await self.async_request("wireless/24/stats")

    async def async_get_wps(self) -> Any:
        return await self.async_request("wireless/wps")

    async def async_on_wps(self) -> Any:
        return await self.async_request("wireless/wps", "post")

    async def async_off_wps(self) -> Any:
        return await self.async_request("wireless/wps", "delete")

    async def async_get_repeater(self) -> Any:
        return await self.async_request("wireless/repeater")

    async def async_wireless_turn_on(self) -> None:
        return await self.async_request("wireless?radio.enable=1", method="put")

    async def async_wireless_turn_off(self) -> None:
        return await self.async_request("wireless?radio.enable=0", method="put")

    async def async_wireless_24_turn_on(self) -> Any:
        return await self.async_request("wireless/24?radio.enable=1", method="put")

    async def async_wireless_5_turn_on(self) -> Any:
        return await self.async_request("wireless/5?radio.enable=1", method="put")

    async def async_wireless_24_turn_off(self) -> Any:
        return await self.async_request("wireless/24?radio.enable=0", method="put")

    async def async_wireless_5_turn_off(self) -> Any:
        return await self.async_request("wireless/5?radio.enable=0", method="put")

    async def async_wireless_guest_turn_on(self) -> Any:
        return await self.async_request("wireless/guestenable?enable=1", method="put")

    async def async_wireless_guest_turn_off(self) -> Any:
        return await self.async_request("wireless/guestenable?enable=0", method="put")

    async def _get_wireless_id(self, mode: str) -> Any:
        wireless = await self.async_request("wireless")
        return wireless.get("ssid", {}).get(mode, {}).get("id")
