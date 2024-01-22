"""Bbox connect."""
from __future__ import annotations

import asyncio
import json
import logging
import socket
from typing import Any

import aiohttp
import async_timeout

from .exceptions import HttpRequestError, ServiceNotFoundError, TimeoutExceededError

_LOGGER = logging.getLogger(__name__)


class BboxRequests:
    """Class request."""

    def __init__(
        self,
        hostname: str = None,
        password: str = None,
        timeout: str = 120,
        session: aiohttp.ClientSession = None,
        use_tls: bool = True,
    ) -> None:
        """Initialize."""
        self.hostname = hostname or "mabbox.bytel.fr"
        self.password = password
        self.needs_auth = self.password is not None

        self._session = session or aiohttp.ClientSession()
        self._timeout = timeout
        scheme = "https" if use_tls else "http"
        self._url = f"{scheme}://{self.hostname}/api"

    async def async_request(
        self,
        method: str,
        url: str,
        data: Any | None = None,
        retry: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Request url with method."""
        try:
            full_url = f"{self._url}/{url}"
            _LOGGER.debug("%s %s %s", method, full_url, data)
            if method == "post":
                token = await self.async_get_token()
                url = f"{url}?btoken={token}"

            async with async_timeout.timeout(self._timeout):
                response = await self._session.request(
                    method, full_url, data=data, **kwargs
                )

        except (asyncio.CancelledError, asyncio.TimeoutError) as error:
            raise TimeoutExceededError(
                "Timeout occurred while connecting to Bbox."
            ) from error
        except (aiohttp.ClientError, socket.gaierror) as error:
            raise HttpRequestError(
                "Error occurred while communicating with Bbox router."
            ) from error

        content_type = response.headers.get("Content-Type", "")
        if response.status // 100 in [4, 5]:
            if response.status == 401 and self.needs_auth:
                await self.async_auth()
                if retry is False:
                    return await self.async_request(
                        method, url, data, retry=True, **kwargs
                    )

            contents = await response.read()
            response.close()
            if content_type == "application/json":
                raise ServiceNotFoundError(
                    response.status, json.loads(contents.decode("utf8"))
                )
            raise ServiceNotFoundError(response.status, contents.decode("utf8"))

        if "application/json" in content_type:
            result = await response.json()
            _LOGGER.debug("Json mode")
            _LOGGER.debug(result)
            return result

        result = await response.text()
        _LOGGER.debug("Text mode")
        _LOGGER.debug(result)
        return result

    async def async_auth(self) -> aiohttp.ClientResponse:
        """Request authentication."""
        if not self.password:
            raise RuntimeError("No password provided!")
        try:
            result = await self._session.request(
                "post", f"{self._url}/v1/login", data={"password": self.password}
            )
            if result.status != 200:
                result.raise_for_status()
        except (aiohttp.ClientError, socket.gaierror) as error:
            raise HttpRequestError("Error occurred while authentication.") from error

    async def async_get_token(self) -> str:
        """Request token."""
        result = await self.async_request("get", "v1/device/token")
        return result["device"]["token"]
