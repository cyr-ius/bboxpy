"""Devices."""

from __future__ import annotations


class Device:
    """Device information."""

    def __init__(self, request):
        """Initialize."""
        self.async_request = request

    async def async_get_bbox_info(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/device")

    async def async_get_bbox_cpu(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/device/cpu")

    async def async_get_bbox_led(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/device/led")

    async def async_get_bbox_mem(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/device/mem")

    async def async_get_bbox_summary(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/device/summary")

    async def async_get_bbox_token(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/device/token")

    async def async_get_bbox_log(self):
        """Fetch data information."""
        return await self.async_request("get", "v1/device/log")

    async def async_reboot(self):
        """Fetch data information."""
        return await self.async_request("post", "v1/device/reboot")

    async def async_reset(self):
        """Fetch data information."""
        return await self.async_request("post", "v1/device/factory")

    async def async_optimization(self, flag: bool):
        """Fetch data information."""
        flag = 1 if flag else 0
        return await self.async_request(
            "put", "v1/device/optimization", {"boolean": flag}
        )

    async def async_display(self, luminosity: int = None, orientation: int = None):
        """Fetch data information."""
        data = {}
        if luminosity:
            data.update({"luminosity": luminosity})
        if orientation:
            data.update({"orientation": orientation})
        return await self.async_request("post", "v1/device/display", data)
