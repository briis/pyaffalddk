# ruff: noqa: F401
"""A Python Wrapper to communicate with AffaldDK API."""

from pyaffalddk.api import GarbageCollection
from pyaffalddk.interface import (
    AffaldDKGarbageTypeNotFound,
    AffaldDKNotSupportedError,
    AffaldDKNotValidAddressError,
    AffaldDKNoConnection,
)
from pyaffalddk.data import PickupEvents, PickupType, AffaldDKAddressInfo

from pyaffalddk.municipalities import (
    SUPPORTED_MUNICIPALITIES,
    MUNICIPALITIES_LIST,
)
from pyaffalddk.const import (
    ICON_LIST,
    NAME_ARRAY,
    NAME_LIST,
    WEEKDAYS,
    WEEKDAYS_SHORT,
)

__title__ = "pyaffalddk"
__version__ = "2.12.2"
__author__ = "briis"
__license__ = "MIT"
