"""Provides API access to Bouygues Bbox."""
from .device import Device
from .lan import Lan
from .wan import Wan
from .ddns import Ddns
from .voip import VOIP
from .iptv import IPTv

__all__ = ["Device", "Lan", "Wan", "VOIP", "IPTv", "Ddns"]
