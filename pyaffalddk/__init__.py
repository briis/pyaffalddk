# ruff: noqa: F401
"""A Python Wrapper to communicate with AffaldDK API."""

from __future__ import annotations

from pyaffalddk.api import (
    GarbageCollection,
    AffaldDKGarbageTypeNotFound,
    AffaldDKNotSupportedError,
    AffaldDKNotValidAddressError,
    AffaldDKNoConnection,
)
from pyaffalddk.data import PickupEvents, PickupType, AffaldDKAddressInfo

from pyaffalddk.municipalities import (
    MUNICIPALITIES_ARRAY,
)
from pyaffalddk.const import (
    ICON_LIST,
    NAME_ARRAY,
    NAME_LIST,
)

__title__ = "pyaffalddk"
__version__ = "2.4.0"
__author__ = "briis"
__license__ = "MIT"
