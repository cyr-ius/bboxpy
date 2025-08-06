"""Tests connection."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
import json
from unittest.mock import AsyncMock, patch

import pytest

from bboxpy import AuthorizationError, Bbox, ServiceNotFoundError, TimeoutExceededError
from bboxpy.auth import BboxRequests

from . import load_fixture, mock_error, mock_error_auth, mock_json

TOKEN = {
    "token": "test_token",
    "expires": (datetime.now() + timedelta(hours=1)).isoformat(),
}
OLD_TOKEN = {
    "token": "test_token",
    "expires": (datetime.now() - timedelta(days=1)).isoformat(),
}


@pytest.fixture
def bbox_instance():
    return load_fixture("device.json").encode("utf-8")


@pytest.mark.asyncio
async def test_async_auth_success() -> None:
    """Test connect."""
    with patch("aiohttp.ClientSession.request", new_callable=mock_json) as mock:
        bbox = Bbox(password="password")
        await bbox.async_login()

    assert len(mock.mock_calls) == 3
    assert bbox._authenticated is True


@pytest.mark.asyncio
async def test_async_auth_no_password() -> None:
    """Test connect."""
    with (
        patch("aiohttp.ClientSession.request", new_callable=mock_json) as mock,
        pytest.raises(RuntimeError, match="No password provided!"),
    ):
        bbox = Bbox(password=None)
        await bbox.async_login()

    assert len(mock.mock_calls) == 0
    assert bbox._authenticated is False


@pytest.mark.asyncio
async def test_async_request_success() -> None:
    """Test connect."""
    with (
        patch("aiohttp.ClientSession.request", new_callable=mock_json) as mock,
        patch("bboxpy.auth.BboxRequests.async_get_token", return_value=TOKEN["token"]),
    ):
        bbox = Bbox(password="password")
        response = await bbox.async_request("test_path")

    assert len(mock.mock_calls) == 3
    assert bbox._authenticated is False
    assert response["raw"] == "raw content"


@pytest.mark.asyncio
async def test_async_request_timeout():
    with (
        patch("aiohttp.ClientSession.request", side_effect=asyncio.TimeoutError),
        pytest.raises(
            TimeoutExceededError, match="Timeout occurred while connecting to Bbox"
        ),
    ):
        bbox = Bbox(password="password")
        await bbox.async_request("test_path")


@pytest.mark.asyncio
async def test_async_login_timeout():
    with (
        patch("aiohttp.ClientSession.request", side_effect=asyncio.TimeoutError),
        pytest.raises(
            AuthorizationError, match="Timeout occurred while connecting to Bbox."
        ),
    ):
        bbox = Bbox(password="password")
        await bbox.async_login()


@pytest.mark.asyncio
async def test_async_request_authorization_error():
    with (
        patch("aiohttp.ClientSession.request", new_callable=mock_error_auth),
        patch("bboxpy.auth.BboxRequests.async_get_token", return_value=TOKEN["token"]),
        pytest.raises(AuthorizationError, match=r"Authorization failed \(401\)"),
    ):
        bbox = Bbox(password="password")
        await bbox.async_request("test_path")


@pytest.mark.asyncio
async def test_async_request_raise_for_status():
    with (
        patch("aiohttp.ClientSession.request", new_callable=mock_error),
        patch("bboxpy.auth.BboxRequests.async_get_token", return_value=TOKEN["token"]),
        pytest.raises(ServiceNotFoundError),
    ):
        bbox = Bbox(password="test_password")
        await bbox.async_request("test_path")


@pytest.mark.asyncio
async def test_async_get_token_success() -> None:
    with (
        patch(
            "bboxpy.auth.BboxRequests.async_auth", new_callable=AsyncMock
        ) as mock_auth,
        patch(
            "bboxpy.auth.BboxRequests.async_request", new_callable=AsyncMock
        ) as mock_request,
    ):
        mock_request.return_value = [{"device": TOKEN}]

        bbox_requests = BboxRequests("password")
        token = await bbox_requests.async_get_token()
        assert token == "test_token"
        mock_auth.assert_called_once()
        mock_request.assert_called_once_with("device/token")


@pytest.mark.asyncio
async def test_async_get_device_info(bbox_instance) -> None:
    with (
        patch("bboxpy.auth.BboxRequests.async_get_token", return_value=TOKEN["token"]),
        patch("aiohttp.ClientSession.request", new_callable=mock_json) as mock_request,
    ):
        mock_request.return_value.read.return_value = bbox_instance
        bbox = Bbox(password="test_password")
        response = await bbox.device.async_get_bbox_summary()

        assert response == json.loads(bbox_instance)
        mock_request.assert_called_once_with(
            "get",
            "https://mabbox.bytel.fr/api/v1/device/summary",
            params={"btoken": "test_token"},
        )


@pytest.mark.asyncio
async def test_async_request_retry():
    with (
        patch("aiohttp.ClientSession.request", new_callable=mock_error) as mock,
        patch("bboxpy.auth.BboxRequests.async_get_token", return_value=TOKEN["token"]),
    ):
        mock.return_value.json.return_value = {
            "exception": {"errors": [{"reason": "Cannot extract request parameters"}]}
        }
        bbox = Bbox(password="test_password")
        with pytest.raises(TimeoutExceededError):
            await bbox.async_request("test_path")
