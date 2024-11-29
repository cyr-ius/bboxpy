"""Bbox connect."""

from __future__ import annotations

import asyncio
import json
import logging
import socket
from typing import Any, cast, Optional
from datetime import datetime

from aiohttp import ClientError, ClientResponse, ClientResponseError, ClientSession

from .exceptions import HttpRequestError, ServiceNotFoundError, TimeoutExceededError

_LOGGER = logging.getLogger(__name__)

API_VERSION = "api/v1"


class BboxRequests:
    """Class request."""

    _authenticated: bool = False
    _btoken: Optional[dict[str, Any]] = None

    def __init__(
        self,
        password: str,
        hostname: str = "mabbox.bytel.fr",
        timeout: int = 120,
        session: ClientSession = None,
        use_tls: bool = True,
    ) -> None:
        """Initialize."""
        self.password = password
        self._session = session
        self._timeout = timeout
        scheme = "https" if use_tls else "http"
        self._uri = f"{scheme}://{hostname}/{API_VERSION}"

    async def async_request(self, path: str, method: str = "get", **kwargs: Any) -> Any:
        """Request url with method."""
        try:
            url = f"{self._uri}/{path}"

            if path not in ["login", "device/token"]:
                token = await self.async_get_token()
                url = f"{url}?btoken={token}"

            async with asyncio.timeout(self._timeout):
                _LOGGER.debug("Request: %s (%s) - %s", url, method, kwargs.get("json"))
                response = await self._session.request(method, url, **kwargs)
                contents = (await response.read()).decode("utf8")
        except (asyncio.CancelledError, asyncio.TimeoutError) as error:
            raise TimeoutExceededError(
                "Timeout occurred while connecting to Bbox."
            ) from error
        except (ClientError, socket.gaierror) as error:
            raise HttpRequestError(
                "Error occurred while communicating with Bbox router."
            ) from error

        try:
            response.raise_for_status()
        except ClientResponseError as err:
            if "application/json" in response.headers.get("Content-Type", ""):
                raise ServiceNotFoundError(
                    response.status, json.loads(contents)
                ) from err
            raise

        return (
            await response.json()
            if "application/json" in response.headers.get("Content-Type", "")
            else await response.text()
        )

    async def async_auth(self) -> ClientResponse:
        """Request authentication."""
        if not self.password:
            raise RuntimeError("No password provided!")
        if self._authenticated:
            return True
        await self.async_request(
            "login", "post", data={"password": self.password, "remember": 1}
        )
        self._authenticated = True

    async def async_get_token(self) -> str:
        """Request token."""
        if self._btoken:
            if not self._btoken["expires"] < datetime.now().astimezone():
                _LOGGER.debug(
                    "Previously retrieved Bbox token always valid (expire on %s), use it",
                    self._btoken["expires"],
                )
                return cast(str, self._btoken["token"])
            _LOGGER.debug(
                "Bbox token expired since %s, renewing it", self._btoken["expires"]
            )

        # Ensure we are authenticated
        await self.async_auth()

        result = await self.async_request("device/token")
        self._btoken = {
            "token": result[0]["device"]["token"],
            "expires": datetime.fromisoformat(result[0]["device"]["expires"]),
        }
        return cast(str, self._btoken["token"])
