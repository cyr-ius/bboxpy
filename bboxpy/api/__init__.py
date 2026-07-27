"""Provides API access to Bouygues Bbox."""

from .ddns import Ddns
from .device import Device
from .iptv import IPTv
from .lan import Lan
from .parentalcontrol import ParentalControl
from .remote import Remote
from .services import Services
from .speedtest import Speedtest
from .voip import VOIP
from .wan import Wan
from .wifi import Wifi

__all__ = [
    "VOIP",
    "Ddns",
    "Device",
    "IPTv",
    "Lan",
    "ParentalControl",
    "Remote",
    "Services",
    "Speedtest",
    "Wan",
    "Wifi",
]
