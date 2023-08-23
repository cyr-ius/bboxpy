"""Provides API access to Bouygues Bbox."""
from .device import Device
from .lan import Lan
from .wan import Wan

__all__ = ["Device", "Lan", "Wan"]
