import pytest
from aiohttp import ClientSession
from pyaffalddk import GarbageCollection


@pytest.mark.asyncio
async def test_Aalborg(capsys):
    with capsys.disabled():
        session = ClientSession()
        gc = GarbageCollection('Aalborg', session=session)

        address = await gc.get_address_id('9000', 'Boulevarden', '13')
        add = {'address_id': '139322', 'kommunenavn': 'Aalborg', 'vejnavn': 'Boulevarden', 'husnr': '13'}
        # print(address.__dict__)
        assert address.__dict__ == add

        pickups = await gc.get_pickup_data(address.address_id)
        assert len(pickups) > 1
        assert 'next_pickup' in pickups


@pytest.mark.asyncio
async def test_Odense(capsys):
    with capsys.disabled():
        session = ClientSession()
        gc = GarbageCollection('Odense', session=session)

        address = await gc.get_address_id('5000', 'Flakhaven', '2')
        # print(address.__dict__)
        add = {'address_id': '112970', 'kommunenavn': 'Odense', 'vejnavn': 'Flakhaven', 'husnr': '2'}
        assert address.__dict__ == add

        pickups = await gc.get_pickup_data(address.address_id)
        assert len(pickups) > 1


@pytest.mark.asyncio
async def test_Aarhus(capsys):
    with capsys.disabled():
        session = ClientSession()
        gc = GarbageCollection('Aarhus', session=session)

        address = await gc.get_address_id('8000', 'Rådhuspladsen', '2')
        # print(address.__dict__)
        add = {'address_id': '07517005___2_______', 'kommunenavn': 'Aarhus', 'vejnavn': 'Rådhuspladsen', 'husnr': '2'}
        assert address.__dict__ == add

        pickups = await gc.get_pickup_data(address.address_id)
        assert len(pickups) > 1
        assert 'next_pickup' in pickups


@pytest.mark.asyncio
async def test_Kbh(capsys):
    with capsys.disabled():
        session = ClientSession()
        gc = GarbageCollection('København', session=session)

        address = await gc.get_address_id('1550', 'Rådhuspladsen', '1')
        # print(address.__dict__)
        add = {'address_id': 'a4e9a503-c27f-ef11-9169-005056823710', 'kommunenavn': 'København', 'vejnavn': 'Rådhuspladsen', 'husnr': '1'}
        assert address.__dict__ == add

        pickups = await gc.get_pickup_data(address.address_id)
        assert len(pickups) > 1
        assert 'next_pickup' in pickups
