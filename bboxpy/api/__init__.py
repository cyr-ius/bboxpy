"""Provides API access to Bouygues Bbox."""

from .ddns import Ddns
from .device import Device
from .iptv import IPTv
from .lan import Lan
from .voip import VOIP
from .wan import Wan
from .parentalcontrol import ParentalControl

__all__ = ["Ddns", "Device", "IPTv", "Lan", "ParentalControl", "VOIP", "Wan"]
