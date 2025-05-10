"""This module contains the code to get garbage data from AffaldDK."""

import datetime as dt
from ical.calendar_stream import IcsCalendarStream
from ical.exceptions import CalendarParseError
import json
import logging
import re
from urllib.parse import urlparse, parse_qsl
from typing import Any
import base64
import aiohttp

from .const import (
    GH_API,
    ICON_LIST,
    MATERIAL_LIST,
    NAME_LIST,
    NON_MATERIAL_LIST,
    NON_SUPPORTED_ITEMS,
    PAR_EXCEPTIONS,
    STRIPS,
    SUPPORTED_ITEMS,
    WEEKDAYS,
)
from .municipalities import MUNICIPALITIES_IDS, MUNICIPALITIES_LIST
from .data import PickupEvents, PickupType, AffaldDKAddressInfo


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

    def __init__(self, session=None) -> None:
        """Initialize the class."""
        self.session = session
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def async_get_request(self, url, headers=None, para=None, as_json=True, new_session=False):
        return await self.async_api_request('GET', url, headers, para, as_json, new_session)

    async def async_post_request(self, url, headers={"Content-Type": "application/json"}, para=None, as_json=True, new_session=False):
        return await self.async_api_request('POST', url, headers, para, as_json, new_session)

    async def async_api_request(self, method, url, headers, para=None, as_json=True, new_session=False) -> dict[str, Any]:
        """Make an API request."""

        if new_session:
            session = aiohttp.ClientSession()
        else:
            session = self.session

        data = None
        if method == 'POST':
            json_input = para
            data_input = None
        else:
            json_input = None
            data_input = para

        async with session.request(method, url, headers=headers, json=json_input, data=data_input) as response:
            if response.status != 200:
                if new_session:
                    await session.close()

                if response.status == 400:
                    raise AffaldDKNotSupportedError(
                        "Municipality not supported")

                if response.status == 404:
                    raise AffaldDKNotSupportedError(
                        "Municipality not supported")

                if response.status == 503:
                    raise AffaldDKNoConnection(
                        "System API is currently not available")

                raise AffaldDKNoConnection(
                    f"Error {response.status} from {url}")

            if as_json:
                data = await response.json()
            else:
                data = await response.text()
            if new_session:
                await session.close()

            return data


class NemAffaldAPI(AffaldDKAPIBase):
    # NemAffaldService API
    def __init__(self, domain, session=None):
        super().__init__(session)
        self._token = None
        self._id = None
        self.street = None
        self.base_url = f'https://nemaffaldsservice.{domain}.dk'

    @property
    async def token(self):
        if self._token is None:
            await self._get_token()
        return self._token

    async def _get_token(self):
        data = ''
        async with self.session.get(self.base_url) as response:
            data = await response.text()

        if data:
            match = re.search(
                r'name="__RequestVerificationToken"\s+[^>]*value="([^"]+)"', data)
            if match:
                self._token = match.group(1)

    async def get_address_id(self, zipcode, street, house_number):
        if self._id is None:
            data = {
                '__RequestVerificationToken': await self.token,
                'SearchTerm': f"{street} {house_number}"
            }
            async with self.session.post(f"{self.base_url}/WasteHome/SearchCustomerRelation", data=data) as response:
                if len(response.history) > 1:
                    o = urlparse(response.history[1].headers['Location'])
                    self._id = dict(parse_qsl(o.query))['customerId']
        return self._id

    async def async_get_ical_data(self, customerid):
        ics_data = ''
        data = {'customerId': customerid, 'type': 'ics'}
        async with self.session.get(f"{self.base_url}/Calendar/GetICaldendar", data=data) as response:
            ics_data = await response.text()
        return ics_data

    async def get_garbage_data(self, address_id):
        return await self.async_get_ical_data(address_id)


class PerfectWasteAPI(AffaldDKAPIBase):
    # Perfect Waste API
    def __init__(self, municipality_id, session=None):
        super().__init__(session)
        self.baseurl = "https://europe-west3-perfect-waste.cloudfunctions.net"
        self.url_data = self.baseurl + "/getAddressCollections"
        self.url_search = self.baseurl + "/searchExternalAddresses"
        self.municipality_id = municipality_id

    async def get_address_id(self, zipcode, street, house_number):
        body = {'data': {
            "query": f"{street} {house_number}, {zipcode}",
            "municipality": self.municipality_id,
            "page": 1, "onlyManual": False
            }}
        data = await self.async_post_request(self.url_search, para=body)
        if len(data['result']) == 1:
            address_id = data['result'][0]['addressID']
            await self.save_to_db(address_id)
            return address_id
        return None

    async def save_to_db(self, address_id):
        url = self.baseurl + '/fetchAddressAndSaveToDb'
        para = {"data": {
            "addressID": address_id, "municipality": self.municipality_id,
            "caretakerCode": None, "isCaretaker": None}}
        await self.async_post_request(url, para=para)

    async def get_garbage_data(self, address_id):
        body = {"data": {
            "addressID": address_id,
            "municipality": self.municipality_id
            }}
        data = await self.async_post_request(self.url_data, para=body)
        return data["result"]


class RenowebghAPI(AffaldDKAPIBase):
    # Renoweb servicegh API
    def __init__(self, municipality_id, session=None):
        super().__init__(session)
        self.url_data = "https://servicesgh.renoweb.dk/v1_13/"
        self.uuid = base64.b64decode(GH_API).decode('utf-8')
        self.headers = {'Accept-Encoding': 'gzip'}
        self.municipality_id = municipality_id
        self.info = {}

    async def get_road(self, zipcode, street):
        url = self.url_data + 'GetJSONRoad.aspx'
        data = {
            'apikey': self.uuid, 'municipalitycode': self.municipality_id,
            'roadname': street
        }
        js = await self.async_get_request(url, para=data, headers=self.headers)
        for item in js['list']:
            if str(zipcode) in item['name']:
                return item['id']
        return None

    async def get_address(self, road_id, house_number):
        url = self.url_data + 'GetJSONAdress.aspx'
        data = {
            'apikey': self.uuid, 'municipalitycode': self.municipality_id,
            'roadid': road_id, 'streetBuildingIdentifier': house_number,
            }
        js = await self.async_get_request(url, para=data, headers=self.headers)
        for item in js['list']:
            if str(house_number) == str(item['streetBuildingIdentifier']):
                return item
        return None

    async def get_address_id(self, zipcode, street, house_number):
        road_id = await self.get_road(zipcode, street)
        if road_id:
            self.info = await self.get_address(road_id, house_number)
            if self.info:
                return self.info['id']
        return None

    async def get_garbage_data(self, address_id, fullinfo=0, shared=0):
        url = self.url_data + 'GetJSONContainerList.aspx'
        data = {
            'apikey': self.uuid, 'municipalitycode': self.municipality_id,
            'adressId': address_id, 'fullinfo': fullinfo, 'supportsSharedEquipment': shared,
            }
        js = await self.async_get_request(url, para=data, headers=self.headers)
        if js:
            return js['list']
        return []


class AarhusAffaldAPI(AffaldDKAPIBase):
    # Aarhus Forsyning API
    def __init__(self, session=None):
        super().__init__(session)
        self.url_data = "https://portal-api.kredslob.dk/api/calendar/address/"
        self.url_search = "https://api.dataforsyningen.dk/adresser?kommunekode=751&q="

    async def get_address_id(self, zipcode, street, house_number):
        url = f"{self.url_search}{street.capitalize()}*"
        _LOGGER.debug("URL: %s", url)
        data: dict[str, Any] = await self.async_get_request(url)
        _result_count = len(data)
        if _result_count > 1:
            for row in data:
                if (
                    str(zipcode) in row["adgangsadresse"]["postnummer"]["nr"]
                    and str(house_number) == row["adgangsadresse"]["husnr"]
                ):
                    return row["kvhx"]
        return None

    async def get_garbage_data(self, address_id):
        url = f"{self.url_data}{address_id}"
        data = await self.async_get_request(url)
        return data[0]["plannedLoads"]


class OdenseAffaldAPI(AffaldDKAPIBase):
    # Odense Renovation API
    def __init__(self, session=None):
        super().__init__(session)
        self.url_data = "https://mit.odenserenovation.dk/api/Calendar/GetICalCalendar?addressNo="
        self.url_search = "https://mit.odenserenovation.dk/api/Calendar/CommunicationHouseNumbers?addressString="

    async def async_get_ical_data(self, address_id) -> dict[str, Any]:
        """Get data from iCal API."""
        url = f"{self.url_data}{address_id}"
        data = await self.async_get_request(url, as_json=False)
        return data

    async def get_address_id(self, zipcode, street, house_number):
        url = f"{self.url_search}{street}"
        data = await self.async_get_request(url)
        for row in data:
            if (
                zipcode in row["PostCode"]
                and house_number == row["FullHouseNumber"]
            ):
                return row["AddressNo"]
        return None

    async def get_garbage_data(self, address_id):
        return await self.async_get_ical_data(address_id)


class AffaldDKAPI(AffaldDKAPIBase):
    # Renoweb API
    """Class to get data from AffaldDK."""

    def __init__(self, session=None):
        super().__init__(session)
        self.url_data = ".renoweb.dk/Legacy/JService.asmx/GetAffaldsplanMateriel_mitAffald"
        self.url_search = ".renoweb.dk/Legacy/JService.asmx/Adresse_SearchByString"

    async def get_address_id(self, municipality_url, zipcode, street, house_number):
        url = f"https://{municipality_url}{self.url_search}"
        body = {
            "searchterm": f"{street} {house_number}",
            "addresswithmateriel": 7,
        }
        # _LOGGER.debug("Municipality URL: %s %s", url, body)
        data = await self.async_post_request(url, para=body)
        result = json.loads(data["d"])
        # _LOGGER.debug("Address Data: %s", result)
        if "list" not in result:
            raise AffaldDKNoConnection(
                f'''AffaldDK API: {
                    result['status']['status']} - {result['status']['msg']}'''
            )

        _result_count = len(result["list"])
        _item: int = 0
        _row_index: int = 0
        if _result_count > 1:
            for row in result["list"]:
                if zipcode in row["label"] and house_number in row["label"]:
                    _item = _row_index
                    break
                _row_index += 1
        address_id = result["list"][_item]["value"]
        if address_id == "0000":
            return None
        return address_id


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
        # self._tzinfo = None
        self._street = None
        self._house_number = None
        self._api_data = None
        self._data = None
        self._municipality_url = None
        self._address_id = None
        self.fail = fail
        self.utc_offset = dt.datetime.now().astimezone().utcoffset()

        for key, value in MUNICIPALITIES_LIST.items():
            if key.lower() == self._municipality.lower():
                self._api_data = value[1]
                if self._api_data == '2':
                    self._api = OdenseAffaldAPI(session=session)
                    self._municipality_url = value[0]
                elif self._api_data == '3':
                    self._api = AarhusAffaldAPI(session=session)
                    self._municipality_url = value[0]
                elif self._api_data == '4':
                    self._api = NemAffaldAPI(value[0], session=session)
                    self._municipality_url = self._api.base_url
                elif self._api_data == '5':
                    self._municipality_url = MUNICIPALITIES_IDS.get(self._municipality.lower(), '')
                    self._api = PerfectWasteAPI(self._municipality_url, session=session)
                elif self._api_data == '6':
                    self._municipality_url = MUNICIPALITIES_IDS.get(self._municipality.lower(), '')
                    self._api = RenowebghAPI(self._municipality_url, session=session)

        if not hasattr(self, '_api'):
            raise RuntimeError(f'Unknow municipality: "{municipality}"')
        if session:
            self._api.session = session

    async def async_init(self) -> None:
        """Initialize the connection."""
        if self._municipality is not None:
            if self._api_data == "2":
                url = f"{self._api.url_search}{self._street}"
                await self._api.async_get_request(url)
            elif self._api_data == "3":
                url = f"{self._api.url_search}{self._street}*"
                await self._api.async_get_request(url)
            elif self._api_data == "4":
                await self._api.token

    async def get_address_id(
        self, zipcode: str, street: str, house_number: str
    ) -> AffaldDKAddressInfo:
        """Get the address id."""

        if self._municipality_url is not None:
            self._address_id = await self._api.get_address_id(zipcode, street, house_number)

            if self._address_id is None:
                raise AffaldDKNotValidAddressError("Address not found")

            address_data = AffaldDKAddressInfo(
                str(self._address_id),
                self._municipality.capitalize(),
                street.capitalize(),
                str(house_number),
            )
            return address_data
        else:
            raise AffaldDKNotSupportedError("Cannot find Municipality")

    async def get_pickup_data(self, address_id: str, debug=False) -> PickupEvents:
        """Get the garbage collection data."""

        if self._municipality_url is not None:
            pickup_events: PickupEvents = {}
            _next_pickup = dt.datetime(2030, 12, 31, 23, 59, 0)
            _next_pickup = _next_pickup.date()
            _next_pickup_event: PickupType = None
            _next_name = []
            _next_description = []

            if self._api_data == "2":
                data = await self._api.get_garbage_data(address_id)
                try:
                    ics = IcsCalendarStream.calendar_from_ics(data)
                    for event in ics.timeline:
                        _garbage_types = split_ical_garbage_types(
                            event.summary)
                        for garbage_type in _garbage_types:
                            _pickup_date = event.start_datetime.date()
                            if _pickup_date < dt.date.today():
                                continue

                            key = get_garbage_type_from_material(
                                garbage_type, self._municipality, address_id, self.fail
                            )
                            _pickup_event = {
                                key: PickupType(
                                    date=_pickup_date,
                                    group=key,
                                    friendly_name=NAME_LIST.get(key),
                                    icon=ICON_LIST.get(key),
                                    entity_picture=f"{key}.svg",
                                    description=garbage_type,
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

                    if _next_name:
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
                        pickup_events.update(_next_pickup_event)
                except CalendarParseError as err:
                    _LOGGER.error("Error parsing iCal data: %s", err)

            elif self._api_data == "3":
                garbage_data = await self._api.get_garbage_data(address_id)
                for row in garbage_data:
                    _pickup_date = iso_string_to_date(row["date"])
                    if _pickup_date < dt.date.today():
                        continue
                    for item in row["fractions"]:
                        key = get_garbage_type_from_material(
                            item, self._municipality, address_id, self.fail
                        )
                        _pickup_event = {
                            key: PickupType(
                                date=_pickup_date,
                                group=key,
                                friendly_name=NAME_LIST.get(key),
                                icon=ICON_LIST.get(key),
                                entity_picture=f"{key}.svg",
                                description=item,
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

                if _next_name:
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
                    pickup_events.update(_next_pickup_event)

            elif self._api_data == "4":
                data = await self._api.get_garbage_data(address_id)
                try:
                    ics = IcsCalendarStream.calendar_from_ics(data)
                    for event in ics.timeline:
                        _garbage_types = split_ical_garbage_types(
                            event.summary)
                        for garbage_type in _garbage_types:
                            _pickup_date = (event.start_datetime + self.utc_offset).date()
                            # _LOGGER.debug(
                            #     "Start Date: %s - End Date: %s", _start_date, _pickup_date)
                            if _pickup_date < dt.date.today():
                                continue

                            key = get_garbage_type(garbage_type)
                            if key == garbage_type:
                                warn_or_fail(garbage_type, self._municipality, address_id, fail=self.fail)
                                continue
                            _pickup_event = {
                                key: PickupType(
                                    date=_pickup_date,
                                    group=key,
                                    friendly_name=NAME_LIST.get(key),
                                    icon=ICON_LIST.get(key),
                                    entity_picture=f"{key}.svg",
                                    description=garbage_type,
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
                    if _next_name:
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
                        pickup_events.update(_next_pickup_event)
                except CalendarParseError as err:
                    _LOGGER.error("Error parsing iCal data: %s", err)

            elif self._api_data == "5":
                garbage_data = await self._api.get_garbage_data(address_id)
                for row in garbage_data:
                    _pickup_date = iso_string_to_date(row["date"])
                    if _pickup_date < dt.date.today():
                        continue
                    for item in row["fractions"]:
                        fraction_name = item['fractionName']
                        key = get_garbage_type(fraction_name)
                        if fraction_name in NON_SUPPORTED_ITEMS:
                            continue
                        if key == fraction_name:
                            warn_or_fail(fraction_name, self._municipality, address_id, fail=self.fail)
                            continue

                        _pickup_event = {
                            key: PickupType(
                                date=_pickup_date,
                                group=key,
                                friendly_name=NAME_LIST.get(key),
                                icon=ICON_LIST.get(key),
                                entity_picture=f"{key}.svg",
                                description=fraction_name,
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
                                _next_description.append(fraction_name)

                if _next_name:
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
                    pickup_events.update(_next_pickup_event)

            elif self._api_data == "6":
                garbage_data = await self._api.get_garbage_data(address_id)
                for item in garbage_data:
                    if not item['nextpickupdatetimestamp']:
                        continue
                    _pickup_date = dt.datetime.fromtimestamp(int(item["nextpickupdatetimestamp"])).date()
                    if _pickup_date < dt.date.today():
                        continue
                    key = get_garbage_type_from_material(
                        item['name'], self._municipality, address_id, self.fail
                    )

                    _pickup_event = {
                        key: PickupType(
                            date=_pickup_date,
                            group=key,
                            friendly_name=NAME_LIST.get(key),
                            icon=ICON_LIST.get(key),
                            entity_picture=f"{key}.svg",
                            description=item['name'],
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
                            _next_description.append(item['name'])

                if _next_name:
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
                    pickup_events.update(_next_pickup_event)

            return pickup_events


def iso_string_to_date(datetext: str) -> dt.date:
    """Convert a date string to a datetime object."""
    if datetext == "Ingen tømningsdato fundet!":
        return None

    return dt.datetime.fromisoformat(datetext).date()


def get_garbage_type(item: str) -> str:
    """Get the garbage type."""
    # _LOGGER.debug("Affalds type: %s", item)
    for key, values in SUPPORTED_ITEMS.items():
        for entry in values:
            if item.lower() == entry.lower():
                return key
    return item


def get_garbage_type_from_material(item, municipality, address_id, fail=False):
    """Get the garbage type from the materialnavn."""
    # _LOGGER.debug("Material: %s", item)
    fixed_item = item.lower()
    if ':' in fixed_item:
        fixed_item = fixed_item.split(':')[1]

    for strip in WEEKDAYS + STRIPS:
        fixed_item = fixed_item.replace(strip.lower(), '')

    escaped = [re.escape(e.lower()) for e in PAR_EXCEPTIONS]
    pattern = rf"\s*\((?!{'|'.join(escaped)}\)).*?\)"
    fixed_item = re.sub(pattern, "", fixed_item)  # strip anything in parenthesis

    fixed_item = fixed_item.strip().rstrip(',').lstrip(', ').rstrip(' - ').lstrip(' - ')
    fixed_item = fixed_item.split(' - ')[0].strip()

    if 'haveaffald' in fixed_item:
        return 'haveaffald'  # Lyngby gives "Haveaffald 1. mar-30. nov"

    if item in NON_MATERIAL_LIST:
        return 'genbrug'
    for key, value in MATERIAL_LIST.items():
        if fixed_item.lower() in str(value).lower():
            for entry in value:
                if fixed_item.lower() == entry.lower():
                    return key
    print(f'\nmissing: "{fixed_item}"')
    warn_or_fail(item, municipality, address_id, source='Material', fail=fail)
    return "genbrug"


def warn_or_fail(name, municipality, address_id, source='Garbage', fail=False):
    msg = f'{source} type [{name}] is not defined in the system for Genbrug. '
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
