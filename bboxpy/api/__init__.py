"""Provides API access to Bouygues Bbox."""

from .ddns import Ddns
from .device import Device
from .iptv import IPTv
from .lan import Lan
from .parentalcontrol import ParentalControl
from .remote import Remote
from .services import Services
from .voip import VOIP
from .wan import Wan
from .wifi import Wifi

__all__ = [
    "Ddns",
    "Device",
    "IPTv",
    "Lan",
    "ParentalControl",
    "VOIP",
    "Wan",
    "Wifi",
    "Services",
    "Remote",
]
