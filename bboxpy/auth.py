"""Bbox connect."""

from __future__ import annotations

import asyncio
from datetime import datetime
import json
import logging
import socket
from typing import Any, cast

from aiohttp import ClientError, ClientResponseError, ClientSession, TCPConnector

from .exceptions import (
    AuthorizationError,
    HttpRequestError,
    ServiceNotFoundError,
    TemporaryError,
    TimeoutExceededError,
)
from .helpers import retry

_LOGGER = logging.getLogger(__name__)

API_VERSION = "api/v1"
TEMPORARY_ERROR_REASONS = ["Cannot extract request parameters"]
DELAY = 1
TRIES = 3


class BboxRequests:
    """Class request."""

    _authenticated: bool = False
    _btoken: dict[str, Any] | None = None

    def __init__(
        self,
        password: str,
        hostname: str | None = None,
        timeout: int | None = None,
        session: ClientSession | None = None,
        use_tls: bool = True,
        verify_ssl: bool = True,
        use_dns_cache: bool = True,
    ) -> None:
        """Initialize."""

        conn = TCPConnector(
            use_dns_cache=use_dns_cache, verify_ssl=verify_ssl, family=socket.AF_INET
        )

        self.password = password
        self._session = session or ClientSession(connector=conn)
        self._timeout = timeout or 120
        self._uri = f"http{'s' if use_tls else ''}://{hostname or 'mabbox.bytel.fr'}/{API_VERSION}"
        self._verify_ssl = verify_ssl

    @retry(exceptions=TemporaryError, tries=TRIES, delay=DELAY, logger=_LOGGER)
    async def async_request(self, path: str, method: str = "get", **kwargs: Any) -> Any:
        """Request url with method."""
        contents = ""
        response = None
        try:
            url = f"{self._uri}/{path}"

            if path not in ["login", "device/token"]:
                token = await self.async_get_token()
                url = f"{url}?btoken={token}"

            async with asyncio.timeout(self._timeout):
                _LOGGER.debug("Request: %s (%s) - %s", url, method, kwargs.get("json"))
                response = await self._session.request(method, url, **kwargs)
                contents = (await response.read()).decode("utf8")
                response.raise_for_status()
        except (asyncio.CancelledError, TimeoutError) as error:
            raise TimeoutExceededError(
                "Timeout occurred while connecting to Bbox."
            ) from error
        except ClientResponseError as error:
            if response and "application/json" in response.headers.get(
                "Content-Type", ""
            ):
                result = await response.json()
                if response.status in [401, 429, 403]:
                    raise AuthorizationError(
                        f"Authorization failed ({response.status})"
                    ) from error
                if (
                    response.status >= 400
                    and isinstance(result, dict)
                    and "exception" in result
                    and isinstance(result["exception"], dict)
                ):
                    for err in result["exception"].get("errors", []):
                        if err.get("reason") in TEMPORARY_ERROR_REASONS:
                            raise TemporaryError(result) from error
                raise ServiceNotFoundError(response.status, result) from error
            raise ServiceNotFoundError(
                response.status if response else "", contents
            ) from error
        except (ClientError, socket.gaierror) as error:
            raise HttpRequestError(
                f"Error occurred while communicating with Bbox router. ({error})"
            ) from error

        result = (
            json.loads(contents)
            if "application/json" in response.headers.get("Content-Type", "")
            else contents
        )
        _LOGGER.debug("Result (%s): %s", response.status, result)
        return result

    async def async_auth(self) -> bool:
        """Request authentication."""
        if not self.password:
            raise RuntimeError("No password provided!")
        if self._authenticated:
            return self._authenticated
        await self.async_request(
            "login", "post", data={"password": self.password, "remember": 1}
        )
        self._authenticated = True

        return self._authenticated

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
