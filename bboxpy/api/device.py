"""Devices."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Device:
    """Device information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_bbox_info(self) -> Any:
        """Fetch data information."""
        return await self.async_request("device")

    async def async_get_bbox_cpu(self) -> Any:
        """Fetch data information."""
        return await self.async_request("device/cpu")

    async def async_get_bbox_led(self) -> Any:
        """Fetch data information."""
        return await self.async_request("device/led")

    async def async_get_bbox_mem(self) -> Any:
        """Fetch data information."""
        return await self.async_request("device/mem")

    async def async_get_bbox_summary(self) -> Any:
        """Fetch data information."""
        return await self.async_request("device/summary")

    async def async_get_bbox_token(self) -> Any:
        """Fetch data information."""
        return await self.async_request("device/token")

    async def async_get_bbox_log(self) -> Any:
        """Fetch data information."""
        return await self.async_request("device/log")

    async def async_reboot(self) -> None:
        """Fetch data information."""
        await self.async_request("device/reboot", "post")

    async def async_reset(self) -> None:
        """Fetch data information."""
        await self.async_request("device/factory", "post")

    async def async_optimization(self, flag: bool) -> None:
        """Fetch data information."""
        await self.async_request(
            "device/optimization", "put", json={"boolean": 1 if flag else 0}
        )

    async def async_display(
        self, luminosity: int | None = None, orientation: int | None = None
    ) -> None:
        """Fetch data information."""
        data = {}
        if luminosity:
            data.update({"luminosity": luminosity})
        if orientation:
            data.update({"orientation": orientation})
        await self.async_request("device/display", "post", json=data)
