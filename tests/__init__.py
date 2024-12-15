"""Tests package."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, Mock

from aiohttp import ClientResponseError
from multidict import CIMultiDict


def mock_factory(status_code=200, resp_data=None):
    data = json.dumps(resp_data)
    mock = AsyncMock()
    mock.return_value.headers = CIMultiDict({("Content-Type", "application/json")})
    mock.return_value.status = status_code
    mock.return_value.json = AsyncMock(return_value=data)
    mock.return_value.text = AsyncMock(return_value=str(data))
    mock.return_value.read = AsyncMock(return_value=data.encode("utf-8"))
    mock.return_value.raise_for_status = Mock()
    if status_code >= 400:
        mock.return_value.raise_for_status = Mock(
            side_effect=ClientResponseError(request_info=None, history=())
        )
    return mock


def mock_json():
    """Mock bbox session request."""
    return mock_factory(resp_data={"raw": "raw content"})


def mock_error():
    """Mock bbox session request."""
    return mock_factory(status_code=400)


def mock_error_auth():
    """Mock bbox session request."""
    return mock_factory(status_code=401)


def load_fixture(filename: str) -> str:
    """Load a fixture."""
    path = Path(__package__) / "fixtures" / filename
    return path.read_text(encoding="utf-8")
