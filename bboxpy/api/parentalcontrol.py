"""Parental Control"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class ParentalControl:
    """Parental control information."""

    def __init__(self, request: Callable[..., Any]) -> None:
        """Initialize."""
        self.async_request = request

    async def async_get_parental_control_service_state(self) -> Any:
        """Get parental control service state."""
        return await self.async_request("parentalcontrol")

    async def async_set_parental_control_service_state(self, enable: bool) -> Any:
        """Set parental control service state."""
        return await self.async_request(
            "parentalcontrol",
            method="put",
            data={"enable": int(enable)},
        )

    async def async_set_device_parental_control_state(
        self, macaddress: str, enable: bool
    ) -> Any:
        """Set device parental control state."""
        return await self.async_request(
            "parentalcontrol/hosts",
            method="put",
            data={"macaddress": macaddress, "enable": int(enable)},
        )
