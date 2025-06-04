import aiohttp
import base64
import datetime as dt
import logging
import re
import json
from urllib.parse import urlparse, parse_qsl, quote
from bs4 import BeautifulSoup

from .const import GH_API


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

    async def async_api_request(self, method, url, headers, para=None, as_json=True, new_session=False):
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

    async def get_address_list(self, zipcode, street, house_number):
        url = self.base_url + '/WasteHome/AddressByTerm'
        para = {'term': f'{street} {house_number}'.strip(), 'limit': 100}
        data = await self.async_get_request(url, para=para, as_json=False)
        return [{'name': item['label'], 'id': item['Id']} for item in json.loads(data)]

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

    async def get_address_list(self, zipcode, street, house_number):
        para = {'term': f'{street} {house_number}'.strip(), 'numberOfResults': 100}
        data = await self.async_get_request(self.url_search, para=para)
        results = [{'name': item['FuldtVejnavn'], 'id': item['Id']} for item in data if str(zipcode) == item['Postnr'] ]
        return results

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

    async def get_address_list(self, zipcode, street, house_number):
        para = {'data': {
            "query": f"{street} {house_number}".strip(),
            "municipality": self.municipality_id,
            "page": 1, "onlyManual": False
            }}

        page = await self.async_post_request(self.url_search, para=para)
        data = page['result']
        while len(page['result']) == 30:
            para['data']['page'] += 1
            page = await self.async_post_request(self.url_search, para=para)
            data += page['result']
        results = [{'name': item['displayName'], 'id': item['addressID']} for item in data if str(zipcode) in item['displayName'] ]
        return results

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

    async def get_address_list(self, zipcode, street, house_number):
        road_id = await self.get_road(zipcode, street)
        if road_id:
            url = self.url_data + 'GetJSONAdress.aspx'
            para = {'apikey': self.uuid, 'municipalitycode': self.municipality_id, 'roadid': road_id}
            if house_number:
                para['streetBuildingIdentifier'] = house_number
            data = await self.async_get_request(url, para=para, headers=self.headers)
            results = [{'name': item['presentationString'], 'id': item['id']} for item in data['list'] if str(zipcode) in item['presentationString'] ]
            return results

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
            info = await self.get_address(road_id, house_number)
            if info:
                return info['id']
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
    # Affald online / Renoweb API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = "https://www.affaldonline.dk/api/address/"
        uuid = base64.b64decode(self.municipality_id).decode('utf-8')
        self.headers = {
            'X-Client-Provider': uuid,
            'X-Client-Type': 'Kunde app',
            'X-Client-Version': '22',
        }

    async def get_address_list(self, zipcode, street, house_number):
        para = {'q': f'{street} {house_number}'.strip(), 'page': 1}
        page = await self.async_get_request(self.url_base + 'search', para=para, headers=self.headers)
        data = page['results']
        while len(page['results']) == 50:
            para['page'] += 1
            page = await self.async_get_request(self.url_base + 'search', para=para, headers=self.headers)
            data += page['results']
        results = [{'name': item['displayName'], 'id': item['addressId']} for item in data if str(zipcode) in item['displayName'] ]
        return results

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


class OpenExperienceAPI(AffaldDKAPIBase):
    # Open Experience API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = f"https://{self.municipality_id}"

    async def get_address_list(self, zipcode, street, house_number):
        address = f'{street} {house_number}'.strip()
        url = self.url_base + f'search/address/{quote(address)}/limit/200'
        data = await self.async_get_request(url)
        results = [{'name': item['displayName'], 'id': item['addressId']} for item in data['results'] if str(zipcode) in item['displayName'] ]
        return results

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


class OpenExperienceLiveAPI(AffaldDKAPIBase):
    # Open Experience API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = "https://live.affaldsapi.dk/"
        uuid = base64.b64decode(self.municipality_id[1:]).decode('utf-8')
        self.headers = {'X-Auth-Token': uuid}
        self.mid = self.municipality_id[0]

    async def get_address_list(self, zipcode, street, house_number):
        address = f'{street} {house_number}'.strip()

        url = self.url_base + f'address/v1/search/{self.mid}/{quote(address)}/100'
        data = await self.async_get_request(url, headers=self.headers)
        results = [{'name': item['name'], 'id': item['id']} for item in data if str(zipcode) in item['name'] ]
        return results

    async def get_address_id(self, zipcode, street, house_number):
        address = quote(f'{street} {house_number}')
        url = self.url_base + f'address/v1/search/{self.mid}/{address}/50'
        data = await self.async_get_request(url, headers=self.headers)
        for res in sorted(data, key=lambda x: x["name"]):
            if str(zipcode) in res['name']:
                return res['id']
        return None

    async def get_garbage_data(self, address_id):
        url = self.url_base + f'arrangements/v1/collections/calendar/{self.mid}/{address_id}'
        data = await self.async_get_request(url, headers=self.headers)
        return data


class ProvasAPI(AffaldDKAPIBase):
    # Provas API (Haderslev)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = "https://platform-api.wastehero.io/api-crm-portal/v1/"
        self._token = None
        self.today = dt.date.today()

    @property
    async def token(self):
        if not self._token:
            vars = {"username": "", "password": ""}
            url = self.url_base + 'company/provas-portal.wastehero.io/login'
            data = await self.async_post_request(url, para=vars)
            self._token = data.get('token')
        return self._token

    async def get_address_list(self, zipcode, street, house_number):
        headers = {'X-API-Key': await self.token}
        address = f'{street} {house_number}, {zipcode}'.strip()
        url = self.url_base + 'property/'
        data = await self.async_get_request(url, para={'search': address, 'limit':100}, headers=headers)
        results = [{'name': item['location']['name'], 'id': item['id']} for item in data if str(zipcode) in item['location']['name'] ]
        return results

    async def get_address_id(self, zipcode, street, house_number):
        headers = {'X-API-Key': await self.token}
        address = f'{street} {house_number}, {zipcode}'
        url = self.url_base + 'property/'
        data = await self.async_get_request(url, para={'search': address}, headers=headers)
        for res in data:
            if str(zipcode) in res['location']['name']:
                return res['id']
        return None

    async def get_garbage_data(self, address_id):
        headers = {'X-API-Key': await self.token}
        url = self.url_base + f'property/{address_id}/collection_log'
        params = {
            'from_date': str(self.today + dt.timedelta(days=-1)),
            'to_date': str(self.today + dt.timedelta(days=60))
        }
        data = await self.async_get_request(url, para=params, headers=headers)
        return data


class RenoDjursAPI(AffaldDKAPIBase):
    # Reno Djurs API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = "https://minside.renodjurs.dk"

    async def get_address_list(self, zipcode, street, house_number):
        address = f'{street} {house_number}*, {zipcode}'.strip()

        url = self.url_base + '/Default.aspx/GetAddress'
        data = await self.async_post_request(url, para={'address': address.strip()})
        results = [{'name': item['label'], 'id': item['value']} for item in data['d'] if str(zipcode) in item['label'] ]
        return results

    async def get_address_id(self, zipcode, street, house_number):
        address = f'{street} {house_number}'
        url = self.url_base + '/Default.aspx/GetAddress'
        data = await self.async_post_request(url, para={'address': address})
        for res in data['d']:
            if str(zipcode) in res['label']:
                return res['value']

    async def get_garbage_data(self, address_id):
        url = self.url_base + '/Ordninger.aspx?id=55424'
        data = await self.async_get_request(url, as_json=False)
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find("table", class_="table--compact")

        headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
        rows = []
        for tr in table.find("tbody").find_all("tr"):
            td = tr.find_all("td")
            if len(td) == len(headers):
                row_data = {h:td.get_text(strip=True) for h, td in zip(headers, td)}
                if row_data['Næste tømningsdag']:
                    rows.append(row_data)
        return rows


class AarhusAffaldAPI(AffaldDKAPIBase):
    # Aarhus Forsyning API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_data = "https://portal-api.kredslob.dk/api/calendar/address/"
        self.url_search = "https://api.dataforsyningen.dk/adresser"

    async def get_address_list(self, zipcode, street, house_number):
        para = {'kommunekode': 751, 'q': f'{street} {house_number}'.strip(), 'struktur': 'mini'}
        data = await self.async_get_request(self.url_search, para=para)
        results = [{'name': item['betegnelse'], 'id': item["id"]} for item in data if str(zipcode) in item["postnr"] ]
        return results

    async def get_address_id(self, zipcode, street, house_number):
        for add in await self.get_address_list(zipcode, street, house_number):
            para = {'kommunekode': 751, 'id': add['id']}
            row = await self.async_get_request(self.url_search, para=para)
            if (
                str(zipcode) in row[0]["adgangsadresse"]["postnummer"]["nr"]
                and str(house_number) == row[0]["adgangsadresse"]["husnr"]
            ):
                return row[0]["kvhx"]
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

    async def get_address_list(self, zipcode, street, house_number):
        address = f'{street} {house_number}'.strip()
        url = f"{self.url_search}{quote(address)}"
        data = await self.async_get_request(url)
        results = [{'name': item['FullAddress'], 'id': item["AddressNo"]} for item in data if str(zipcode) in item["PostCode"] ]
        return results

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

    async def async_get_ical_data(self, address_id):
        """Get data from iCal API."""
        url = f"{self.url_data}{address_id}"
        data = await self.async_get_request(url, as_json=False)
        return data

    async def get_garbage_data(self, address_id):
        return await self.async_get_ical_data(address_id)
