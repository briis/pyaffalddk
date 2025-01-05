"""This module contains the code to get garbage data from AffaldDK."""

from __future__ import annotations

import abc
import datetime as dt
from datetime import timezone
import zoneinfo
from aiozoneinfo import async_get_time_zone as _async_get_time_zone
from functools import lru_cache, partial
from ical.calendar_stream import IcsCalendarStream
from ical.exceptions import CalendarParseError
import json
import logging

from typing import Any

import aiohttp

from .const import (
    API_DATA_LIST,
    ICON_LIST,
    MATERIAL_LIST,
    MUNICIPALITIES_LIST,
    NAME_LIST,
    NON_MATERIAL_LIST,
    NON_SUPPORTED_ITEMS,
    SUPPORTED_ITEMS,
    WEEKDAYS,
)
from .data import PickupEvents, PickupType, AffaldDKAddressInfo

UTC = dt.UTC
UTC_TIME_ZONE: dt.tzinfo = dt.UTC

_LOGGER = logging.getLogger(__name__)


class AffaldDKNotSupportedError(Exception):
    """Raised when the municipality is not supported."""


class AffaldDKNotValidAddressError(Exception):
    """Raised when the address is not found."""


class AffaldDKNoConnection(Exception):
    """Raised when no data is received."""


class AffaldDKGarbageTypeNotFound(Exception):
    """Raised when new garbage type is detected."""


class AffaldDKAPIBase:
    """Base class for the API."""

    @abc.abstractmethod
    async def async_api_request(self, url: str) -> dict[str, Any]:
        """Override this."""
        raise NotImplementedError(
            "users must define async_api_request to use this base class"
        )

@lru_cache(maxsize=1)
def get_denmark_timezone():
    """Get Denmark timezone object safely."""
    return zoneinfo.ZoneInfo("Europe/Copenhagen")

@lru_cache(maxsize=1)
def get_default_time_zone() -> dt.tzinfo:
    """Get the default time zone."""
    return DEFAULT_TIME_ZONE

class AffaldDKAPI(AffaldDKAPIBase):
    """Class to get data from AffaldDK."""

    def __init__(self) -> None:
        """Initialize the class."""
        self.session = None
        self.request_timeout = 10

    async def async_get_time_zone(self, time_zone_str: str) -> zoneinfo.ZoneInfo | None:
        """Get time zone from string. Return None if unable to determine.

        Async friendly.
        """
        try:
            return await _async_get_time_zone(time_zone_str)
        except zoneinfo.ZoneInfoNotFoundError:
            return None

    async def async_api_request(self, url: str, body: str) -> dict[str, Any]:
        """Make an API request."""

        is_new_session = False
        if self.session is None:
            self.session = aiohttp.ClientSession()
            is_new_session = True

        headers = {"Content-Type": "application/json"}

        async with self.session.post(
            url, headers=headers, data=json.dumps(body)
        ) as response:
            if response.status != 200:
                if is_new_session:
                    await self.session.close()

                if response.status == 400:
                    raise AffaldDKNotSupportedError("Municipality not supported")

                if response.status == 404:
                    raise AffaldDKNotSupportedError("Municipality not supported")

                if response.status == 503:
                    raise AffaldDKNoConnection("System API is currently not available")

                raise AffaldDKNoConnection(f"Error {response.status} from {url}")

            data = await response.text()
            if is_new_session:
                await self.session.close()

            json_data = json.loads(data)
            return json_data

    async def async_api_request_2(self, url: str) -> dict[str, Any]:
        """Get data from standard REST API."""

        is_new_session = False
        if self.session is None:
            self.session = aiohttp.ClientSession()
            is_new_session = True

        async with self.session.get(url) as response:
            if response.status != 200:
                if is_new_session:
                    await self.session.close()
                if response.status == 400:
                    raise AffaldDKNotSupportedError("Municipality not supported")
                if response.status == 404:
                    raise AffaldDKNotSupportedError("Municipality not supported")
                if response.status == 500:
                    raise AffaldDKNoConnection("System API is currently not available")

                raise AffaldDKNoConnection(f"Error {response.status} from {url}")

            data = await response.text()
            if is_new_session:
                await self.session.close()

            json_data = json.loads(data)
            return json_data

    async def async_get_ical_data(self, url: str) -> dict[str, Any]:
        """Get data from iCal API."""

        is_new_session = False
        if self.session is None:
            self.session = aiohttp.ClientSession()
            is_new_session = True

        async with self.session.get(url) as response:
            if response.status != 200:
                if is_new_session:
                    await self.session.close()
                if response.status == 400:
                    raise AffaldDKNotSupportedError("Municipality not supported")
                if response.status == 404:
                    raise AffaldDKNotSupportedError("Municipality not supported")
                if response.status == 500:
                    raise AffaldDKNoConnection("System API is currently not available")

                raise AffaldDKNoConnection(f"Error {response.status} from {url}")

            data = await response.text()
            if is_new_session:
                await self.session.close()

            return data


class GarbageCollection:
    """Class to get garbage collection data."""

    def __init__(
        self,
        municipality: str,
        timezone: str = "Europe/Copenhagen",
        session: aiohttp.ClientSession = None,
        api: AffaldDKAPIBase = AffaldDKAPI(),
    ) -> None:
        """Initialize the class."""
        self._municipality = municipality
        self._timezone = get_denmark_timezone()
        self._street = None
        self._house_number = None
        self._api = api
        self._api_data = None
        self._api_url_data = None
        self._api_url_search = None
        self._data = None
        self._municipality_url = None
        self._address_id = None
        if session:
            self._api.session = session
        for key, value in MUNICIPALITIES_LIST.items():
            if key.lower() == self._municipality.lower():
                self._municipality_url = value[0]
                self._api_data = value[1]
                for key, value in API_DATA_LIST.items():
                    if key == self._api_data:
                        self._api_url_data = value[0]
                        self._api_url_search = value[1]
                        break
                break

    async def async_init(self) -> None:
        """Initialize the connection."""
        if self._municipality is not None:
            if self._api_data == "2":
                url = f"{self._api_url_search}{self._street}"
                await self._api.async_api_request_2(url)
            elif self._api_data == "3":
                url = f"{self._api_url_search}{self._street}*"
                await self._api.async_api_request_2(url)
            else:
                url = f"https://{self._municipality_url}{self._api_url_search}"
                body = {
                    "searchterm": f"{self._street} {self._house_number}",
                    "addresswithmateriel": 1,
                }
                await self._api.async_api_request(url, body)

    async def get_address_id(
        self, zipcode: str, street: str, house_number: str
    ) -> AffaldDKAddressInfo:
        """Get the address id."""

        if self._municipality_url is not None:
            if self._api_data == "2":
                url = f"{self._api_url_search}{street}"
                data: dict[str, Any] = await self._api.async_api_request_2(url)
                _result_count = len(data)
                _item: int = 0
                _row_index: int = 0
                if _result_count > 1:
                    for row in data:
                        if (
                            zipcode in row["PostCode"]
                            and house_number == row["FullHouseNumber"]
                        ):
                            self._address_id = row["AddressNo"]
                            break

                if self._address_id is None:
                    raise AffaldDKNotValidAddressError("Address not found")

            elif self._api_data == "3":
                _street_name = street.capitalize()
                url = f"{self._api_url_search}{_street_name}*"
                _LOGGER.debug("URL: %s", url)
                data: dict[str, Any] = await self._api.async_api_request_2(url)
                _result_count = len(data)
                if _result_count > 1:
                    for row in data:
                        if (
                            zipcode in row["adgangsadresse"]["postnummer"]["nr"]
                            and house_number == row["adgangsadresse"]["husnr"]
                        ):
                            self._address_id = row["kvhx"]
                            break

                if self._address_id is None:
                    raise AffaldDKNotValidAddressError("Address not found")
            else:
                url = f"https://{self._municipality_url}{self._api_url_search}"
                body = {
                    "searchterm": f"{street} {house_number}",
                    "addresswithmateriel": 7,
                }
                # _LOGGER.debug("Municipality URL: %s %s", url, body)
                data: dict[str, Any] = await self._api.async_api_request(url, body)
                result = json.loads(data["d"])
                # _LOGGER.debug("Address Data: %s", result)
                if "list" not in result:
                    raise AffaldDKNoConnection(
                        f"AffaldDK API: {result['status']['status']} - {result['status']['msg']}"
                    )

                _result_count = len(result["list"])
                _item: int = 0
                _row_index: int = 0
                if _result_count > 1:
                    for row in result["list"]:
                        if zipcode in row["label"]:
                            _item = _row_index
                            break
                        _row_index += 1
                self._address_id = result["list"][_item]["value"]

                if self._address_id == "0000":
                    raise AffaldDKNotValidAddressError("Address not found")

            address_data = AffaldDKAddressInfo(
                self._address_id,
                self._municipality.capitalize(),
                street.capitalize(),
                house_number,
            )
            return address_data
        else:
            raise AffaldDKNotSupportedError("Cannot find Municipality")

    async def get_pickup_data(self, address_id: str) -> PickupEvents:
        """Get the garbage collection data."""

        if self._municipality_url is not None:
            pickup_events: PickupEvents = {}
            _next_pickup = dt.datetime(2030, 12, 31, 23, 59, 0)
            _next_pickup = _next_pickup.date()
            _next_pickup_event: PickupType = None
            _next_name = []
            _next_description = []
            _last_update = dt.datetime.now(UTC_TIME_ZONE)
            _utc_date =  _last_update #_last_update.replace(tzinfo=_tzutc)
            _utc_timestamp = _utc_date.timestamp()

            if self._api_data == "2":
                self._address_id = address_id
                url = f"{self._api_url_data}{self._address_id}"
                data = await self._api.async_get_ical_data(url)
                # _LOGGER.debug("iCal Data: %s", data)

                try:
                    # Insert standard timezone rules before parsing
                    data = data.replace("END:VTIMEZONE", """BEGIN:STANDARD
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
END:DAYLIGHT
END:VTIMEZONE""")
                    ics = IcsCalendarStream.calendar_from_ics(data)
                    for event in ics.timeline:
                        _garbage_types = split_ical_garbage_types(event.summary)
                        for garbage_type in _garbage_types:
                            _pickup_date = event.start_datetime.date()
                            if _pickup_date < dt.date.today():
                                continue

                            key = get_garbage_type_from_material(
                                garbage_type, self._municipality, self._address_id
                            )
                            _pickup_event = {
                                key: PickupType(
                                    date=_pickup_date,
                                    group=key,
                                    friendly_name=NAME_LIST.get(key),
                                    icon=ICON_LIST.get(key),
                                    entity_picture=f"{key}.svg",
                                    description=garbage_type,
                                    last_updated=_utc_date,
                                    utc_timestamp=_utc_timestamp,
                                )
                            }
                            if not key_exists_in_pickup_events(pickup_events, key):
                                pickup_events.update(_pickup_event)

                            if _pickup_date is not None:
                                if _pickup_date < dt.date.today():
                                    continue
                                if _pickup_date < _next_pickup:
                                    _next_pickup = _pickup_date
                                    _next_name = []
                                    _next_description = []
                                if _pickup_date == _next_pickup:
                                    _next_name.append(NAME_LIST.get(key))
                                    _next_description.append(garbage_type)

                    _next_pickup_event = {
                        "next_pickup": PickupType(
                            date=_next_pickup,
                            group="genbrug",
                            friendly_name=list_to_string(_next_name),
                            icon=ICON_LIST.get("genbrug"),
                            entity_picture="genbrug.svg",
                            description=list_to_string(_next_description),
                            last_updated=_utc_date,
                            utc_timestamp=_utc_timestamp,
                        )
                    }

                    pickup_events.update(_next_pickup_event)

                except CalendarParseError as err:
                    _LOGGER.error("Error parsing iCal data: %s", err)
            elif self._api_data == "3":
                self._address_id = address_id
                url = f"{self._api_url_data}{self._address_id}"
                data = await self._api.async_api_request_2(url)
                garbage_data = data[0]["plannedLoads"]
                for row in garbage_data:
                    _pickup_date = iso_string_to_date(row["date"])
                    if _pickup_date < dt.date.today():
                        continue
                    for item in row["fractions"]:
                        key = get_garbage_type_from_material(
                            item, self._municipality, self._address_id
                        )
                        _pickup_event = {
                            key: PickupType(
                                date=_pickup_date,
                                group=key,
                                friendly_name=NAME_LIST.get(key),
                                icon=ICON_LIST.get(key),
                                entity_picture=f"{key}.svg",
                                description=item,
                                last_updated=_utc_date,
                                utc_timestamp=_utc_timestamp,
                            )
                        }
                        if not key_exists_in_pickup_events(pickup_events, key):
                            pickup_events.update(_pickup_event)

                        if _pickup_date is not None:
                            if _pickup_date < dt.date.today():
                                continue
                            if _pickup_date < _next_pickup:
                                _next_pickup = _pickup_date
                                _next_name = []
                                _next_description = []
                            if _pickup_date == _next_pickup:
                                _next_name.append(NAME_LIST.get(key))
                                _next_description.append(item)

                _next_pickup_event = {
                    "next_pickup": PickupType(
                        date=_next_pickup,
                        group="genbrug",
                        friendly_name=list_to_string(_next_name),
                        icon=ICON_LIST.get("genbrug"),
                        entity_picture="genbrug.svg",
                        description=list_to_string(_next_description),
                        last_updated=_utc_date,
                        utc_timestamp=_utc_timestamp,
                    )
                }
                pickup_events.update(_next_pickup_event)

                return pickup_events
            else:
                self._address_id = address_id
                url = f"https://{self._municipality_url}{self._api_url_data}"
                # _LOGGER.debug("URL: %s", url)
                body = {"adrid": f"{address_id}", "common": "false"}
                # _LOGGER.debug("Body: %s", body)
                data = await self._api.async_api_request(url, body)
                result = json.loads(data["d"])
                garbage_data = result["list"]
                # _LOGGER.debug("Garbage Data: %s", garbage_data)

                for row in garbage_data:
                    if row["ordningnavn"] in NON_SUPPORTED_ITEMS:
                        continue

                    _pickup_date = None
                    if row["toemningsdato"] not in NON_SUPPORTED_ITEMS:
                        _pickup_date = to_date(row["toemningsdato"])
                    elif str(row["toemningsdage"]).capitalize() in WEEKDAYS:
                        _pickup_date = get_next_weekday(row["toemningsdage"])
                    elif find_weekday_in_string(row["toemningsdage"]) != "None":
                        if row["toemningsdato"] not in NON_SUPPORTED_ITEMS:
                            _weekday = find_weekday_in_string(row["toemningsdage"])
                            _pickup_date = get_next_weekday(_weekday)
                        else:
                            _pickup_date = get_next_year_end()
                    else:
                        continue

                    if (
                        any(
                            group in row["ordningnavn"].lower()
                            for group in [
                                "genbrug",
                                "storskrald",
                                "papir og glas/dåser",
                                "miljøkasse/tekstiler",
                            ]
                        )
                        and self._municipality.lower() == "gladsaxe"
                    ):
                        key = get_garbage_type_from_material(
                            row["materielnavn"], self._municipality, self._address_id
                        )
                    elif (
                        any(
                            group in row["ordningnavn"].lower()
                            for group in [
                                "dagrenovation",
                            ]
                        )
                        and self._municipality.lower() == "gribskov"
                    ):
                        key = get_garbage_type_from_material(
                            row["materielnavn"], self._municipality, self._address_id
                        )

                    elif any(
                        group in row["ordningnavn"].lower()
                        for group in [
                            "genbrug",
                            "papir og glas/dåser",
                            "miljøkasse/tekstiler",
                            "standpladser",
                        ]
                    ):
                        key = get_garbage_type_from_material(
                            row["materielnavn"], self._municipality, self._address_id
                        )
                    else:
                        key = get_garbage_type(row["ordningnavn"])

                    if key == row["ordningnavn"] and key != "Bestillerordning":
                        _LOGGER.warning(
                            "Garbage type [%s] is not defined in the system. Please notify the developer. Municipality: %s, Address ID: %s",
                            key,
                            self._municipality,
                            self._address_id,
                        )
                        continue

                    _pickup_event = {
                        key: PickupType(
                            date=_pickup_date,
                            group=row["ordningnavn"],
                            friendly_name=NAME_LIST.get(key),
                            icon=ICON_LIST.get(key),
                            entity_picture=f"{key}.svg",
                            description=row["materielnavn"],
                            last_updated=_utc_date,
                            utc_timestamp=_utc_timestamp,
                        )
                    }
                    pickup_events.update(_pickup_event)

                    if _pickup_date is not None:
                        if _pickup_date < dt.date.today():
                            continue
                        if _pickup_date < _next_pickup:
                            _next_pickup = _pickup_date
                            _next_name = []
                            _next_description = []
                        if _pickup_date == _next_pickup:
                            _next_name.append(NAME_LIST.get(key))
                            _next_description.append(row["materielnavn"])

                _next_pickup_event = {
                    "next_pickup": PickupType(
                        date=_next_pickup,
                        group="genbrug",
                        friendly_name=list_to_string(_next_name),
                        icon=ICON_LIST.get("genbrug"),
                        entity_picture="genbrug.svg",
                        description=list_to_string(_next_description),
                        last_updated=_utc_date,
                        utc_timestamp=_utc_timestamp,
                    )
                }

                pickup_events.update(_next_pickup_event)

            return pickup_events


def to_date(datetext: str) -> dt.date:
    """Convert a date string to a datetime object."""
    if datetext == "Ingen tømningsdato fundet!":
        return None

    index = datetext.rfind(" ")
    if index == -1:
        return None
    _date = dt.datetime.strptime(f"{datetext[index+1:]}", "%d-%m-%Y")
    return _date.date()


def iso_string_to_date(datetext: str) -> dt.date:
    """Convert a date string to a datetime object."""
    if datetext == "Ingen tømningsdato fundet!":
        return None

    return dt.datetime.fromisoformat(datetext).date()


def get_garbage_type(item: str) -> str:
    """Get the garbage type."""
    # _LOGGER.debug("Affalds type: %s", item)
    for key, value in SUPPORTED_ITEMS.items():
        if item.lower() in str(value).lower():
            for entry in value:
                if item.lower() == entry.lower():
                    return key
    return item


def get_garbage_type_from_material(
    item: str, municipality: str, address_id: str
) -> str:
    """Get the garbage type from the materialnavn."""
    # _LOGGER.debug("Material: %s", item)
    for key, value in MATERIAL_LIST.items():
        if item in NON_MATERIAL_LIST:
            continue
        if item.lower() in str(value).lower():
            for entry in value:
                if item.lower() == entry.lower():
                    return key

    _LOGGER.warning(
        "Material type [%s] is not defined in the system for Genbrug. Please notify the developer. Municipality: %s, Address ID: %s",
        item,
        municipality,
        address_id,
    )
    return "genbrug"


def get_next_weekday(weekday: str) -> dt.date:
    weekdays = WEEKDAYS
    current_weekday = dt.datetime.now().weekday()
    target_weekday = weekdays.index(weekday.capitalize())
    days_ahead = (target_weekday - current_weekday) % 7
    next_date: dt.date = dt.datetime.now() + dt.timedelta(days=days_ahead)
    return next_date.date()


def list_to_string(list: list[str]) -> str:
    """Convert a list to a string."""
    return " | ".join(list)


def find_weekday_in_string(text: str) -> str:
    """Loop through each word in a text string and compare with another word."""
    words = text.split()
    for w in words:
        if w.capitalize() in WEEKDAYS:
            return w.capitalize()
    return "None"


def get_next_year_end() -> dt.date:
    """Return December 31 of the next year."""
    today = dt.date.today()
    next_year = today.year + 1
    return dt.date(next_year, 12, 31)


def split_ical_garbage_types(text: str) -> list[str]:
    """Split a text string at every comma and ignore everything from 'på' or if it starts with 'Tømning af'."""
    if text.startswith("Tømning af"):
        text = text[len("Tømning af ") :]
    if "på" in text:
        text = text.split("på")[0]
    return [item.strip() for item in text.split(",")]


def key_exists_in_pickup_events(pickup_events: PickupEvents, key: str) -> bool:
    """Check if a key exists in PickupEvents."""
    return key in pickup_events


def value_exists_in_pickup_events(pickup_events: PickupEvents, value: Any) -> bool:
    """Check if a value exists in PickupEvents."""
    return any(event for event in pickup_events.values() if event == value)
