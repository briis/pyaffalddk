"""This module contains the code to get garbage data from AffaldDK."""

import datetime as dt
from ical.calendar_stream import IcsCalendarStream
from ical.exceptions import CalendarParseError
import json
import logging
import re
from urllib.parse import urlparse, parse_qsl, quote
from typing import Any
import base64
import aiohttp

from .const import (
    GH_API,
    ICON_LIST,
    NAME_LIST,
    NON_SUPPORTED_ITEMS,
    PAR_EXCEPTIONS,
    SPECIAL_MATERIALS,
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

    def __init__(self, municipality_id, session=None) -> None:
        """Initialize the class."""
        self.municipality_id = municipality_id
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

        async with session.request(method, url, headers=headers, json=json_input, params=data_input) as response:
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token = None
        self._id = None
        self.street = None
        self.base_url = f'https://nemaffaldsservice.{self.municipality_id}.dk'

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


class VestForAPI(AffaldDKAPIBase):
    # Vest Forbrænding API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baseurl = "https://selvbetjening.vestfor.dk"
        self.url_data = self.baseurl + "/Home/MinSide"
        self.url_search = self.baseurl + "/Adresse/AddressByName"
        self.today = dt.date.today()

    async def get_address_id(self, zipcode, street, house_number):
        para = {'term': f'{street} {house_number}, {zipcode}', 'numberOfResults': 50}
        data = await self.async_get_request(self.url_search, para=para, as_json=True)
        if len(data) == 1:
            return data[0]['Id']
        return None

    async def get_garbage_data(self, address_id):
        para = {'address-selected-id': address_id}
        _ = await self.async_get_request(self.url_data, para=para, as_json=False)
        url = 'https://selvbetjening.vestfor.dk/Adresse/ToemmeDates'
        para = {
            'start': str(self.today + dt.timedelta(days=-1)),
            'end': str(self.today + dt.timedelta(days=60))
            }
        data = await self.async_get_request(url, para=para)
        return data


class PerfectWasteAPI(AffaldDKAPIBase):
    # Perfect Waste API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baseurl = "https://europe-west3-perfect-waste.cloudfunctions.net"
        self.url_data = self.baseurl + "/getAddressCollections"
        self.url_search = self.baseurl + "/searchExternalAddresses"

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_data = "https://servicesgh.renoweb.dk/v1_13/"
        self.uuid = base64.b64decode(GH_API).decode('utf-8')
        self.headers = {'Accept-Encoding': 'gzip'}
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


class AffaldOnlineAPI(AffaldDKAPIBase):
    # Affald online API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = "https://www.affaldonline.dk/api/address/"
        uuid = base64.b64decode(self.municipality_id).decode('utf-8')
        self.headers = {
            'X-Client-Provider': uuid,
            'X-Client-Type': 'Kunde app',
            'X-Client-Version': '22',
        }

    async def get_address_id(self, zipcode, street, house_number):
        para = {'q': f'{street} {house_number}'}
        data = await self.async_get_request(self.url_base + 'search', para=para, headers=self.headers)
        for res in data['results']:
            if str(zipcode) in res['displayName']:
                return res['addressId']
        return None

    async def get_garbage_data(self, address_id):
        para = {'groupBy': 'date', 'addressId': address_id}
        data = await self.async_get_request(self.url_base + 'collections', para=para, headers=self.headers)
        return data


class RevasAPI(AffaldDKAPIBase):
    # Revas Viborg API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = "https://dagrenovation.viborg.dk/app/AppService/"

    async def get_address_id(self, zipcode, street, house_number):
        address = quote(f'{street} {house_number}, {zipcode}')
        url = self.url_base + f'search/address/{address}/limit/50'
        data = await self.async_get_request(url)
        for res in sorted(data['results'], key=lambda x: x["addressId"]):
            if str(zipcode) in res['displayName']:
                return res['addressId']
        return None

    async def get_garbage_data(self, address_id):
        url = self.url_base + f'address/{address_id}/collections'
        data = await self.async_get_request(url)
        return data


class AarhusAffaldAPI(AffaldDKAPIBase):
    # Aarhus Forsyning API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


APIS = {
    'odense': OdenseAffaldAPI,
    'aarhus': AarhusAffaldAPI,
    'nemaffald': NemAffaldAPI,
    'perfectwaste': PerfectWasteAPI,
    'renoweb': RenowebghAPI,
    'vestfor': VestForAPI,
    'affaldonline': AffaldOnlineAPI,
    'viborg': RevasAPI,
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

            elif self._api_type == "viborg":
                garbage_data = await self._api.get_garbage_data(address_id)
                for item in garbage_data['collections']:
                    dt_list = [iso_string_to_date(d) for d in item['dates']]
                    if dt_list:
                        _pickup_date = min([d for d in dt_list if d >= self.today])
                        fraction_name = item['fraction']['name']
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

    for fixed_item in clean_fraction_string(item):
        if fixed_item in [non.lower() for non in NON_SUPPORTED_ITEMS]:
            return 'not-supported'
        for key, values in SUPPORTED_ITEMS.items():
            for entry in values:
                if fixed_item.lower() == entry.lower():
                    return key
    print(f'\nmissing: "{fixed_item}"')
    warn_or_fail(item, municipality, address_id, fail=fail)
    return 'missing-type'


def clean_fraction_string(item):
    fixed_item = item.lower()

    for strip in WEEKDAYS + STRIPS:
        fixed_item = fixed_item.replace(strip.lower(), '')

    escaped = [re.escape(e.lower()) for e in PAR_EXCEPTIONS]
    pattern = rf"\s*\((?!{'|'.join(escaped)}\)).*?\)"
    fixed_item = re.sub(pattern, "", fixed_item)  # strip anything in parenthesis

    fixed_item = re.sub(r'\bdistrikt [A-Za-z0-9]\b', '', fixed_item)
    fixed_item = re.sub(r'\brute [0-9]\b', '', fixed_item)
    fixed_item = re.sub(r'\bs[0-9]\b', '', fixed_item) # remove " S6 " Rebild

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
