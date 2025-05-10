import pytest
from freezegun import freeze_time
from aiohttp import ClientSession
from pyaffalddk import GarbageCollection, NAME_LIST
from pathlib import Path
import pickle
import json
from ical.calendar_stream import IcsCalendarStream


UPDATE = False


datadir = Path(__file__).parent/'data'
kbh_ics_data = (datadir/'kbh_ics.data').read_text()
odense_ics_data = (datadir/'odense_ics.data').read_text()
aalborg_data_gh = json.loads((datadir/'Aalborg_gh.data').read_text())
aarhus_data = json.loads((datadir/'Aarhus.data').read_text())
koege_data = json.loads((datadir/'Koege.data').read_text())
FREEZE_TIME = "2025-04-25"
compare_file = (datadir/'compare_data.p')


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
            gc = GarbageCollection('Køge', session=session, fail=True)

            address = await gc.get_address_id('4600', 'Torvet', '1')
            add = {
                'uid': 'Køge_27768', 'address_id': '27768',
                'kommunenavn': 'Køge', 'vejnavn': 'Torvet', 'husnr': '1'}
            # print(address.__dict__)
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return koege_data["result"]
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Koege', pickups, False)


@pytest.mark.asyncio
@freeze_time("2025-05-04")
async def test_Aalborg_gh(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Aalborg', session=session, fail=True)

            address = await gc.get_address_id('9000', 'Boulevarden', '13')
            add = {
                'uid': 'Aalborg_139322', 'address_id': '139322',
                'kommunenavn': 'Aalborg', 'vejnavn': 'Boulevarden', 'husnr': '13'}
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
            gc = GarbageCollection('Odense', session=session, fail=True)

            address = await gc.get_address_id('5000', 'Flakhaven', '2')
            # print(address.__dict__)
            add = {
                'uid': 'Odense_112970', 'address_id': '112970',
                'kommunenavn': 'Odense', 'vejnavn': 'Flakhaven', 'husnr': '2'}
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return odense_ics_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Odense', pickups, UPDATE)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Aarhus(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Aarhus', session=session, fail=True)

            address = await gc.get_address_id('8000', 'Rådhuspladsen', '2')
            # print(address.__dict__)
            add = {
                'uid': 'Aarhus_07517005___2_______', 'address_id': '07517005___2_______',
                'kommunenavn': 'Aarhus', 'vejnavn': 'Rådhuspladsen', 'husnr': '2'}
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return aarhus_data[0]["plannedLoads"]
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Aarhus', pickups, UPDATE)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Kbh(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('København', session=session, fail=True)

            address = await gc.get_address_id('1550', 'Rådhuspladsen', '1')
            # print(address.__dict__)
            add = {
                'uid': 'København_a4e9a503-c27f-ef11-9169-005056823710',
                'address_id': 'a4e9a503-c27f-ef11-9169-005056823710',
                'kommunenavn': 'København', 'vejnavn': 'Rådhuspladsen', 'husnr': '1'}
            assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return kbh_ics_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(address.address_id)
            update_and_compare('Kbh', pickups, UPDATE)
            assert pickups['next_pickup'].description == 'Rest/Madaffald'
            assert pickups['next_pickup'].date.strftime('%d/%m/%y') == '05/05/25'
            assert list(pickups.keys()) == ['restaffaldmadaffald', 'farligtaffald', 'next_pickup']


@pytest.mark.asyncio
@freeze_time("2025-05-09")
async def test_smoketest(capsys, monkeypatch, update=False):
    with capsys.disabled():
        async with ClientSession() as session:
            smokedata = pickle.load((datadir / 'smoketest_garbage_data.p').open('rb'))
            smokecompare_file = datadir / 'smoketest_fractions.json'
            with smokecompare_file.open('r') as fh:
                smokecompare = json.load(fh)

            for name, val in smokedata.items():
                city = val['city']
                gc = GarbageCollection(city, session=session, fail=True)

                async def get_data(*args, **kwargs):
                    return val['data']
                monkeypatch.setattr(gc._api, "get_garbage_data", get_data)
                pickups = await gc.get_pickup_data(1111)
                keys = list(pickups.keys())

                assert set(keys[:-1]).issubset(NAME_LIST)
                assert keys[-1] == 'next_pickup'

                data = {key: pickups[key].description for key in keys[:-1]}
                if name not in smokecompare or update:
                    smokecompare[name] = data
                    print(f'adding "{name}" to the smoketest compare data')
                    with smokecompare_file.open('w', encoding="utf-8") as fh:
                        json.dump(smokecompare, fh, indent=2, ensure_ascii=False)
                if smokecompare[name] != data:
                    print(name, city)
                    print(data)
                    print(smokecompare[name])
                assert smokecompare[name] == data


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
