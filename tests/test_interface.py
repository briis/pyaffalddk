import pytest
from freezegun import freeze_time
from aiohttp import ClientSession
from pyaffalddk import GarbageCollection
from pathlib import Path
import pickle
import json
import os


CI = os.getenv("CI") == "true"
skip_in_ci = pytest.mark.skipif(CI, reason="Skipped in CI environment")
UPDATE = False


datadir = Path(__file__).parent/'data'
kbh_ics_data = (datadir/'kbh_ics.data').read_text()
odense_ics_data = (datadir/'odense_ics.data').read_text()
aalborg_data_gh = json.loads((datadir/'Aalborg_gh.data').read_text())
aarhus_data = json.loads((datadir/'Aarhus.data').read_text())
koege_data = json.loads((datadir/'Koege.data').read_text())
affaldonline_data = json.loads((datadir/'affaldonline.data').read_text())
vestfor_data = pickle.loads((datadir/'vestfor.data').read_bytes())
openexp_data = json.loads((datadir/'openexp.data').read_text())
openexplive_data = json.loads((datadir/'openexplive.data').read_text())
renodjurs_data = json.loads((datadir/'renodjurs.data').read_text())
provas_data = json.loads((datadir/'provas.data').read_text())

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
@freeze_time("2025-05-25")
async def test_OpenExpLive(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Frederiksberg', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Frederiksberg_70984', 'address_id': '70984',
                'kommunenavn': 'Frederiksberg', 'vejnavn': 'Smallegade', 'husnr': '1'}
            if not CI:
                address = await gc.get_address_id('2000', 'Smallegade', '1')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return openexplive_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Frederiksberg', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time("2025-05-20")
async def test_OpenExp(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Viborg', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Viborg_67580', 'address_id': '67580',
                'kommunenavn': 'Viborg', 'vejnavn': 'Prinsens alle', 'husnr': '5'}
            if not CI:
                address = await gc.get_address_id('8800', 'Prinsens Alle', '5')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return openexp_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Viborg', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time("2025-05-20")
async def test_Affaldonline(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Vejle', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Vejle_1261533|490691026|0', 'address_id': '1261533|490691026|0',
                'kommunenavn': 'Vejle', 'vejnavn': 'Klostergade', 'husnr': '2A'}
            if not CI:
                address = await gc.get_address_id('7100', 'Klostergade', '2A')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return affaldonline_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Vejle', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time("2025-05-04")
async def test_Koege(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Køge', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Køge_27768', 'address_id': '27768',
                'kommunenavn': 'Køge', 'vejnavn': 'Torvet', 'husnr': '1'}
            if not CI:
                address = await gc.get_address_id('4600', 'Torvet', '1')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return koege_data["result"]
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Koege', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time("2025-05-04")
async def test_Aalborg_gh(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Aalborg', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Aalborg_139322', 'address_id': '139322',
                'kommunenavn': 'Aalborg', 'vejnavn': 'Boulevarden', 'husnr': '13'}
            if not CI:
                address = await gc.get_address_id('9000', 'Boulevarden', '13')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return aalborg_data_gh
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Aalborg_gh', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Odense(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Odense', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Odense_112970', 'address_id': '112970',
                'kommunenavn': 'Odense', 'vejnavn': 'Flakhaven', 'husnr': '2'}
            if not CI:
                address = await gc.get_address_id('5000', 'Flakhaven', '2')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return odense_ics_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Odense', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Aarhus(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Aarhus', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Aarhus_07517005___2_______', 'address_id': '07517005___2_______',
                'kommunenavn': 'Aarhus', 'vejnavn': 'Rådhuspladsen', 'husnr': '2'}
            if not CI:
                address = await gc.get_address_id('8000', 'Rådhuspladsen', '2')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return aarhus_data[0]["plannedLoads"]
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Aarhus', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time("2025-05-18")
async def test_VestFor(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Ballerup', session=session, fail=True)

            add = {
                'uid': 'Ballerup_2690c90b-016f-e511-80cd-005056be6a4c',
                'address_id': '2690c90b-016f-e511-80cd-005056be6a4c',
                'kommunenavn': 'Ballerup', 'vejnavn': 'Banegårdspladsen', 'husnr': '1'}
            if not CI:
                address = await gc.get_address_id('2750', 'Banegårdspladsen', '1')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return vestfor_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Ballerup', pickups, UPDATE)


@pytest.mark.asyncio
@freeze_time("2025-06-04")
async def test_Provas(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Haderslev', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Haderslev_UHJvcGVydHlUeXBlOjEwMTQzNDE=', 'address_id': 'UHJvcGVydHlUeXBlOjEwMTQzNDE=', 
                'kommunenavn': 'Haderslev', 'vejnavn': 'Christian x vej', 'husnr': '29'
                }
            if not CI:
                address = await gc.get_address_id('6100', "Christian X Vej", '29')
    #            print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return provas_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Haderslev', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time("2025-06-04")
async def test_RenoDjurs(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('Norddjurs', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'Norddjurs_40130', 'address_id': '40130', 
                'kommunenavn': 'Norddjurs', 'vejnavn': 'Torvet', 'husnr': '3'
                }
            if not CI:
                address = await gc.get_address_id('8500', 'Torvet', '3')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return renodjurs_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Norddjurs', pickups, UPDATE)
            print('done: ', gc._municipality)


@pytest.mark.asyncio
@freeze_time(FREEZE_TIME)
async def test_Kbh(capsys, monkeypatch):
    with capsys.disabled():
        async with ClientSession() as session:
            gc = GarbageCollection('København', session=session, fail=True)
            print('start: ', gc._municipality)

            add = {
                'uid': 'København_a4e9a503-c27f-ef11-9169-005056823710',
                'address_id': 'a4e9a503-c27f-ef11-9169-005056823710',
                'kommunenavn': 'København', 'vejnavn': 'Rådhuspladsen', 'husnr': '1'}
            if not CI:
                address = await gc.get_address_id('1550', 'Rådhuspladsen', '1')
                # print(address.__dict__)
                assert address.__dict__ == add

            async def get_data(*args, **kwargs):
                return kbh_ics_data
            monkeypatch.setattr(gc._api, "get_garbage_data", get_data)

            pickups = await gc.get_pickup_data(add['address_id'])
            update_and_compare('Kbh', pickups, UPDATE)
            assert pickups['next_pickup'].description == 'Rest/Madaffald'
            assert pickups['next_pickup'].date.strftime('%d/%m/%y') == '05/05/25'
            assert list(pickups.keys()) == ['restaffaldmadaffald', 'farligtaffald', 'next_pickup']
            print('done: ', gc._municipality)
