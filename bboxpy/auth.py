"""Bbox connect."""

from __future__ import annotations

import asyncio
import json
import logging
import socket
from typing import Any, cast

from aiohttp import ClientError, ClientResponse, ClientResponseError, ClientSession

from .exceptions import HttpRequestError, ServiceNotFoundError, TimeoutExceededError

_LOGGER = logging.getLogger(__name__)

API_VERSION = "api/v1"


class BboxRequests:
    """Class request."""

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
        except ClientResponseError:
            if "application/json" in response.headers.get("Content-Type", ""):
                raise ServiceNotFoundError(response.status, json.loads(contents))
            raise ServiceNotFoundError(response.status, contents)
        except (ClientError, socket.gaierror) as error:
            raise HttpRequestError(
                "Error occurred while communicating with Bbox router."
            ) from error

        return (
            await response.json()
            if "application/json" in response.headers.get("Content-Type", "")
            else await response.text()
        )

    async def async_auth(self) -> ClientResponse:
        """Request authentication."""
        if not self.password:
            raise RuntimeError("No password provided!")
        await self.async_request("login", "post", json={"password": self.password})

    async def async_get_token(self) -> str:
        """Request token."""
        result = await self.async_request("device/token")
        return cast(str, result["device"]["token"])
