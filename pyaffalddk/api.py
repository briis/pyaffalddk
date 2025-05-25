"""This module contains the code to get garbage data from AffaldDK."""

import datetime as dt
from ical.calendar_stream import IcsCalendarStream
from ical.exceptions import CalendarParseError
import logging
import re
from typing import Any
import aiohttp

from .const import (
    ICON_LIST,
    NAME_LIST,
    NON_SUPPORTED_ITEMS,
    PAR_EXCEPTIONS,
    RE_WORDS,
    RE_RAW,
    SPECIAL_MATERIALS,
    STRIPS,
    SUPPORTED_ITEMS,
    WEEKDAYS,
)
from .municipalities import MUNICIPALITIES_IDS, MUNICIPALITIES_LIST
from .data import PickupEvents, PickupType, AffaldDKAddressInfo
from pyaffalddk import interface

_LOGGER = logging.getLogger(__name__)


APIS = {
    'odense': interface.OdenseAffaldAPI,
    'aarhus': interface.AarhusAffaldAPI,
    'nemaffald': interface.NemAffaldAPI,
    'perfectwaste': interface.PerfectWasteAPI,
    'renoweb': interface.RenowebghAPI,
    'vestfor': interface.VestForAPI,
    'affaldonline': interface.AffaldOnlineAPI,
    'openexp': interface.OpenExperienceAPI,
    'openexplive': interface.OpenExperienceLiveAPI,
}


class GarbageCollection:
    """Class to get garbage collection data."""

    def __init__(
        self,
        municipality: str,
        session: aiohttp.ClientSession = None,
        fail: bool = False,
    ) -> None:
        """Initialize the class."""
        self._municipality = municipality
        self._street = None
        self._house_number = None
        self._api_type = None
        self._address_id = None
        self.fail = fail
        self.utc_offset = dt.datetime.now().astimezone().utcoffset()

        municipality_id = MUNICIPALITIES_IDS.get(self._municipality.lower(), '')

        for key, value in MUNICIPALITIES_LIST.items():
            if key.lower() == self._municipality.lower():
                self._api_type = value[0]
                if len(value) > 1:
                    municipality_id = value[1]
                self._api = APIS[self._api_type](municipality_id, session=session)

        if self._api_type is None:
            raise RuntimeError(f'Unknow municipality: "{municipality}"')

    async def async_init(self) -> None:
        """Initialize the connection."""
        if self._municipality is not None:
            if self._api_type == "nemaffald":
                await self._api.token

    async def get_address_id(
        self, zipcode: str, street: str, house_number: str
    ) -> AffaldDKAddressInfo:
        """Get the address id."""

        if self._api_type is not None:
            self._address_id = await self._api.get_address_id(zipcode, street, house_number)

            if self._address_id is None:
                raise interface.AffaldDKNotValidAddressError("Address not found")

            address_data = AffaldDKAddressInfo(
                str(self._address_id),
                self._municipality.capitalize(),
                street.capitalize(),
                str(house_number),
            )
            return address_data
        else:
            raise interface.AffaldDKNotSupportedError("Cannot find Municipality")

    def update_pickup_event(self, item_name, address_id, _pickup_date):
        if _pickup_date < self.today:
            return 'old-event'

        key = get_garbage_type(item_name, self._municipality, address_id, self.fail)
        if key in ['not-supported', 'missing-type']:
            return key

        if (key not in self.pickup_events) or (_pickup_date < self.pickup_events[key].date):
            _pickup_event = {
                key: PickupType(
                    date=_pickup_date,
                    group=key,
                    friendly_name=NAME_LIST.get(key),
                    icon=ICON_LIST.get(key),
                    entity_picture=f"{key}.svg",
                    description=item_name,
                )
            }
            self.pickup_events.update(_pickup_event)
        return 'done'

    def set_next_event(self):
        if not self.pickup_events:
            return
        _next_pickup = min(event.date for event in self.pickup_events.values())
        _next_name = [event.friendly_name for event in self.pickup_events.values() if event.date == _next_pickup]
        _next_description = [event.description for event in self.pickup_events.values() if event.date == _next_pickup]
        _next_pickup_event = {
            "next_pickup": PickupType(
                date=_next_pickup,
                group="genbrug",
                friendly_name=list_to_string(_next_name),
                icon=ICON_LIST.get("genbrug"),
                entity_picture="genbrug.svg",
                description=list_to_string(_next_description),
            )
        }
        self.pickup_events.update(_next_pickup_event)

    async def get_pickup_data(self, address_id: str, debug=False) -> PickupEvents:
        """Get the garbage collection data."""

        if self._api_type is not None:
            self.pickup_events: PickupEvents = {}
            self.today = dt.date.today()

            if self._api_type == 'odense':
                data = await self._api.get_garbage_data(address_id)
                try:
                    ics = IcsCalendarStream.calendar_from_ics(data)
                    for event in ics.timeline:
                        _garbage_types = split_ical_garbage_types(
                            event.summary)
                        for garbage_type in _garbage_types:
                            _pickup_date = event.start_datetime.date()
                            self.update_pickup_event(garbage_type, address_id, _pickup_date)
                except CalendarParseError as err:
                    _LOGGER.error("Error parsing iCal data: %s", err)

            elif self._api_type == "aarhus":
                garbage_data = await self._api.get_garbage_data(address_id)
                for row in garbage_data:
                    _pickup_date = iso_string_to_date(row["date"])
                    if _pickup_date < dt.date.today():
                        continue
                    for garbage_type in row["fractions"]:
                        self.update_pickup_event(garbage_type, address_id, _pickup_date)

            elif self._api_type == "nemaffald":
                data = await self._api.get_garbage_data(address_id)
                try:
                    ics = IcsCalendarStream.calendar_from_ics(data)
                    for event in ics.timeline:
                        _garbage_types = split_ical_garbage_types(
                            event.summary)
                        for garbage_type in _garbage_types:
                            _pickup_date = (event.start_datetime + self.utc_offset).date()
                            self.update_pickup_event(garbage_type, address_id, _pickup_date)

                except CalendarParseError as err:
                    _LOGGER.error("Error parsing iCal data: %s", err)

            elif self._api_type == "perfectwaste":
                garbage_data = await self._api.get_garbage_data(address_id)
                for row in garbage_data:
                    _pickup_date = iso_string_to_date(row["date"])
                    if _pickup_date < dt.date.today():
                        continue
                    for item in row["fractions"]:
                        garbage_type = item['fractionName']
                        self.update_pickup_event(garbage_type, address_id, _pickup_date)

            elif self._api_type == "renoweb":
                garbage_data = await self._api.get_garbage_data(address_id)
                for item in garbage_data:
                    if not item['nextpickupdatetimestamp']:
                        continue
                    _pickup_date = dt.datetime.fromtimestamp(int(item["nextpickupdatetimestamp"])).date()
                    self.update_pickup_event(item['name'], address_id, _pickup_date)

            elif self._api_type == "vestfor":
                garbage_data = await self._api.get_garbage_data(address_id)
                for item in garbage_data:
                    _pickup_date = iso_string_to_date(item['start'])
                    self.update_pickup_event(item['title'], address_id, _pickup_date)

            elif self._api_type == "affaldonline":
                garbage_data = await self._api.get_garbage_data(address_id)
                for item in garbage_data:
                    _pickup_date = iso_string_to_date(item['date'])
                    for garbage_type in item['collections']:
#                        fraction_name = garbage_type['fraction']['name']
                        fraction_description = garbage_type['containers'][0]['description']
#                        print(fraction_name, fraction_description)
                        self.update_pickup_event(fraction_description, address_id, _pickup_date)

            elif self._api_type == "openexp":
                garbage_data = await self._api.get_garbage_data(address_id)
                for item in garbage_data['collections']:
                    dt_list = [iso_string_to_date(d) for d in item['dates']]
                    if dt_list:
                        _pickup_date = min([d for d in dt_list if d >= self.today])
                        fraction_name = item['fraction']['name']
                        self.update_pickup_event(fraction_name, address_id, _pickup_date)

            elif self._api_type == "openexplive":
                garbage_data = await self._api.get_garbage_data(address_id)
                for item in garbage_data:
                    fraction_name = item['fraction']['name']
                    dt_list = [iso_string_to_date(d['date']) for d in item['upcoming_dates']]
                    if dt_list:
                        _pickup_date = min([d for d in dt_list if d >= self.today])
                        self.update_pickup_event(fraction_name, address_id, _pickup_date)

            self.set_next_event()
            return self.pickup_events


def iso_string_to_date(datetext: str) -> dt.date:
    """Convert a date string to a datetime object."""
    if datetext == "Ingen tømningsdato fundet!":
        return None

    return dt.datetime.fromisoformat(datetext).date()


def get_garbage_type(item, municipality, address_id, fail=False):
    """Get the garbage type."""
    # _LOGGER.debug("Affalds type: %s", item)
    if item in NON_SUPPORTED_ITEMS:
        return 'not-supported'

    for special in SPECIAL_MATERIALS:
        if special.lower() in item.lower():
            return SPECIAL_MATERIALS[special]

    fixed_items = clean_fraction_string(item)
    for fixed_item in fixed_items:
        if fixed_item in [non.lower() for non in NON_SUPPORTED_ITEMS]:
            return 'not-supported'
        for key, values in SUPPORTED_ITEMS.items():
            for entry in values:
                if fixed_item.lower() == entry.lower():
                    return key
    print(f'\nmissing: {fixed_items}')
    warn_or_fail(item, municipality, address_id, fail=fail)
    return 'missing-type'


def clean_fraction_string(item):
    fixed_item = item.lower()

    for strip in WEEKDAYS + STRIPS:
        fixed_item = fixed_item.replace(strip.lower(), '')

    escaped = [re.escape(e.lower()) for e in PAR_EXCEPTIONS]
    pattern = rf"\s*\((?!{'|'.join(escaped)}\)).*?\)"
    fixed_item = re.sub(pattern, "", fixed_item)  # strip anything in parenthesis

    for word in RE_RAW:
        fixed_item = re.sub(word, '', fixed_item)
    for word in RE_WORDS:
        fixed_item = re.sub(fr'(?:\s|\b){word}(?=\s|$)', '', fixed_item)

    if ':' in fixed_item:
        fixed_item = fixed_item.split(':')[1]

    fixed_item = fixed_item.strip().rstrip(',').lstrip(', ').rstrip(' -').lstrip('- ').lstrip('*')
    res = [fixed_item.strip()]
    if ' - ' in fixed_item:
        res += [o.strip() for o in fixed_item.split(' - ')]
    return res


def warn_or_fail(name, municipality, address_id, fail=False):
    msg = f'Garbage type [{name}] is not defined in the system. '
    msg += f'Please notify the developer. Municipality: {municipality}, Address ID: {address_id}'

    if fail:
        raise RuntimeError(msg)
    _LOGGER.warning(msg)


def list_to_string(list: list[str]) -> str:
    """Convert a list to a string."""
    return " | ".join(list)


def split_ical_garbage_types(text: str) -> list[str]:
    """Split a text string at every comma and ignore everything from 'på' or if it starts with 'Tømning af'."""
    if text.startswith("Tømning af"):
        text = text[len("Tømning af "):]
    if "på" in text:
        text = text.split("på")[0]
    return [item.strip() for item in text.split(",")]


def key_exists_in_pickup_events(pickup_events: PickupEvents, key: str) -> bool:
    """Check if a key exists in PickupEvents."""
    return key in pickup_events


def value_exists_in_pickup_events(pickup_events: PickupEvents, value: Any) -> bool:
    """Check if a value exists in PickupEvents."""
    return any(event for event in pickup_events.values() if event == value)
