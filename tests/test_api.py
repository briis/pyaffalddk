import pytest
from freezegun import freeze_time
from aiohttp import ClientSession
from pyaffalddk import GarbageCollection
from pyaffalddk.api import AffaldDKAPI
from pathlib import Path
from datetime import datetime
import pickle
import json
from ical.calendar_stream import IcsCalendarStream


UPDATE = False


datadir = Path(__file__).parent/'data'
kbh_ics_data = (datadir/'kbh_ics.data').read_text()
odense_ics_data = (datadir/'odense_ics.data').read_text()
aalborg_data = json.loads((datadir/'Aalborg.data').read_text())
aalborg_data_gh = json.loads((datadir/'Aalborg_gh.data').read_text())
aarhus_data = json.loads((datadir/'Aarhus.data').read_text())
koege_data = json.loads((datadir/'Koege.data').read_text())
FREEZE_TIME = "2025-04-25"
compare_file = (datadir/'compare_data.p')


utc_offset = datetime.now().astimezone().utcoffset()


def update_and_compare(name, actual_data, update=False, debug=False):
    compare_data = pickle.load(compare_file.open('rb'))
    if update:
        compare_data[name] = actual_data
        pickle.dump(compare_data, compare_file.open('wb'))
    if debug and actual_data != compare_data[name]:
        print(actual_data.keys())
        print(compare_data[name].keys())
    assert actual_data == compare_data[name]


@pytest.mark.asyncio
@freeze_time("2025-05-04")
async def test_Koege(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Køge', session=session)

            address = await gc.get_address_id('4600', 'Torvet', '1')
            add = {'address_id': '27768', 'kommunenavn': 'Køge', 'vejnavn': 'Torvet', 'husnr': '1'}
            # print(address.__dict__)
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return koege_data
            monkeypatch.setattr(gc._api, "async_api_request", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Koege', pickups, False)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Aalborg(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Aalborg', session=session)
            gc._api = AffaldDKAPI(session=session)
            gc._municipality_url = 'aalborg'
            gc._api_data = '1'

            address = await gc.get_address_id('9000', 'Boulevarden', '13')
            add = {'address_id': '139322', 'kommunenavn': 'Aalborg', 'vejnavn': 'Boulevarden', 'husnr': '13'}
            # print(address.__dict__)
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return aalborg_data
            monkeypatch.setattr(gc._api, "async_api_request", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Aalborg', pickups, UPDATE)


@pytest.mark.asyncio
@freeze_time("2025-05-04")
async def test_Aalborg_gh(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Aalborg', session=session)

            address = await gc.get_address_id('9000', 'Boulevarden', '13')
            add = {'address_id': 139322, 'kommunenavn': 'Aalborg', 'vejnavn': 'Boulevarden', 'husnr': '13'}
            # print(address.__dict__)
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return aalborg_data_gh
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Aalborg_gh', pickups, UPDATE)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Odense(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Odense', session=session)

            address = await gc.get_address_id('5000', 'Flakhaven', '2')
            # print(address.__dict__)
            add = {'address_id': '112970', 'kommunenavn': 'Odense', 'vejnavn': 'Flakhaven', 'husnr': '2'}
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return odense_ics_data
            monkeypatch.setattr(gc._api, "async_get_ical_data", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Odense', pickups, UPDATE)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Aarhus(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Aarhus', session=session)

            address = await gc.get_address_id('8000', 'Rådhuspladsen', '2')
            # print(address.__dict__)
            add = {'address_id': '07517005___2_______', 'kommunenavn': 'Aarhus', 'vejnavn': 'Rådhuspladsen', 'husnr': '2'}
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return aarhus_data
            monkeypatch.setattr(gc._api, "async_api_request", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Aarhus', pickups, UPDATE)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Kbh(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('København', session=session)

            address = await gc.get_address_id('1550', 'Rådhuspladsen', '1')
            # print(address.__dict__)
            add = {'address_id': 'a4e9a503-c27f-ef11-9169-005056823710', 'kommunenavn': 'København', 'vejnavn': 'Rådhuspladsen', 'husnr': '1'}
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return kbh_ics_data
            monkeypatch.setattr(gc._api, "async_get_ical_data", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Kbh', pickups, UPDATE)
            assert pickups['next_pickup'].description == 'Rest/Madaffald'
            assert pickups['next_pickup'].date.strftime('%d/%m/%y') == '05/05/25'
            assert list(pickups.keys()) == ['restaffaldmadaffald', 'farligtaffald', 'next_pickup']


def test_ics(capsys):
    with capsys.disabled():
        ics = IcsCalendarStream.calendar_from_ics(odense_ics_data)
        data = odense_ics_data.replace("END:VTIMEZONE", """BEGIN:STANDARD
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
        ics2 = IcsCalendarStream.calendar_from_ics(data)
        assert ics.events == ics2.events