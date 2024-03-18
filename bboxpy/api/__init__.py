"""Provides API access to Bouygues Bbox."""

from .ddns import Ddns
from .device import Device
from .iptv import IPTv
from .lan import Lan
from .voip import VOIP
from .wan import Wan

__all__ = ["Device", "Lan", "Wan", "VOIP", "IPTv", "Ddns"]
