"""Devices."""

from __future__ import annotations

from typing import Any, Callable


class Device:
    """Device information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_bbox_info(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/device")

    async def async_get_bbox_cpu(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/device/cpu")

    async def async_get_bbox_led(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/device/led")

    async def async_get_bbox_mem(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/device/mem")

    async def async_get_bbox_summary(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/device/summary")

    async def async_get_bbox_token(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/device/token")

    async def async_get_bbox_log(self) -> Any:
        """Fetch data information."""
        return await self.async_request("get", "v1/device/log")

    async def async_reboot(self) -> None:
        """Fetch data information."""
        await self.async_request("post", "v1/device/reboot")

    async def async_reset(self) -> None:
        """Fetch data information."""
        await self.async_request("post", "v1/device/factory")

    async def async_optimization(self, flag: bool) -> None:
        """Fetch data information."""
        int_flag = 1 if flag else 0
        await self.async_request("put", "v1/device/optimization", {"boolean": int_flag})

    async def async_display(
        self, luminosity: int | None = None, orientation: int | None = None
    ) -> None:
        """Fetch data information."""
        data = {}
        if luminosity:
            data.update({"luminosity": luminosity})
        if orientation:
            data.update({"orientation": orientation})
        await self.async_request("post", "v1/device/display", data)
