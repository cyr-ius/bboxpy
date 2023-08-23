"""Bbox connect."""
from __future__ import annotations

import asyncio
import json
import socket
from typing import Any

import aiohttp
import async_timeout

from .exceptions import HttpRequestError, ServiceNotFoundError, TimeoutExceededError


class BboxRequests:
    """Class request."""

    def __init__(
        self,
        hostname: str = None,
        password: str = None,
        timeout: str = 120,
        session: aiohttp.ClientSession = None,
    ) -> None:
        """Initialize."""
        self.hostname = hostname or "https://mabbox.bytel.fr"
        self.password = password
        self.needs_auth = self.password is not None

        self._session = session or aiohttp.ClientSession()
        self._timeout = timeout
        self._url = f"{self.hostname}/api"

    async def async_request(
        self,
        method: str,
        url: str,
        data: Any | None = None,
        **kwargs: Any,
    ) -> Any:
        """Request url with method."""
        try:
            url = f"{self._url}/{url}"
            if method == "POST":
                token = await self.async_get_token()
                url = f"{url}?btoken={token}"

            async with async_timeout.timeout(self._timeout):
                response = await self._session.request(method, url, data=data, **kwargs)
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
            if response.status_code == 401 and self.needs_auth:
                await self.async_auth()
                if kwargs.get("retry") is False:
                    await self.async_request(method, url, data, retry=True, **kwargs)

            contents = await response.read()
            response.close()
            if content_type == "application/json":
                raise ServiceNotFoundError(
                    response.status, json.loads(contents.decode("utf8"))
                )
            raise ServiceNotFoundError(response.status, contents.decode("utf8"))

        if "application/json" in content_type:
            return await response.json()

        return await response.text()

    async def async_auth(self) -> aiohttp.ClientResponse:
        """Request authentification."""
        if not self.password:
            raise RuntimeError("No password provided!")
        try:
            result = await self._session.request(
                "post", f"{self._url}/apiv1/login", data={"password": self.password}
            )
            if result.status_code != 200:
                result.raise_for_status()
        except (aiohttp.ClientError, socket.gaierror) as error:
            raise HttpRequestError("Error occurred while authentification.") from error
        finally:
            await self._session.close()

    async def async_get_token(self) -> str:
        """Request token."""
        result = await self.async_request("GET", "v1/device/token")
        return result["device"]["token"]
