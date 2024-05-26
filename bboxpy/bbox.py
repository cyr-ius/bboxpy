"""Bbox API."""

from __future__ import annotations

import inspect

from aiohttp import ClientSession

from . import api as Api
from .auth import BboxRequests
from .exceptions import AuthorizationError, BboxException


class Bbox(BboxRequests):
    """API Bouygues Bbox router."""

    def __init__(
        self,
        password: str,
        hostname: str = "mabbox.bytel.fr",
        timeout: int = 120,
        session: ClientSession = ClientSession(),
        use_tls: bool = True,
    ) -> None:
        """Initialize."""
        super().__init__(hostname, password, timeout, session, use_tls)
        self._load_modules()

    def _load_modules(self) -> None:
        """Instantiate modules."""
        for name, obj in Api.__dict__.items():
            if inspect.isclass(obj):
                setattr(self, name.lower(), obj(self.async_request))

    async def async_login(self) -> None:
        """Login."""
        try:
            await self.async_auth()
        except BboxException as error:
            raise AuthorizationError(error) from error

    async def async_logout(self) -> None:
        """Logout."""
        await self.async_request("logout", "post")

    async def async_close(self) -> None:
        """Close the session."""
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> Bbox:
        """Asynchronous enter."""
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit."""
        await self.async_close()
