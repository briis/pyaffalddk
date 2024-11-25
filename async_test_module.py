# ruff: noqa: F401
"""This module is only used to run some realtime data tests using the async functions, while developing the module."""

from __future__ import annotations

import asyncio
import aiohttp
import logging
import time
import sys

from pyaffalddk import (
    GarbageCollection,
    MUNICIPALITIES_ARRAY,
    NAME_ARRAY,
    AffaldDKAddressInfo,
    PickupEvents,
    AffaldDKNoConnection,
)

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Async test module."""

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("ical").setLevel(logging.WARNING)
    start = time.time()

    session = aiohttp.ClientSession()
    garbage = GarbageCollection(municipality=sys.argv[2], session=session)

    if sys.argv[1] == "address_id":
        try:
            address_data: AffaldDKAddressInfo = await garbage.get_address_id(
                zipcode=sys.argv[3], street=sys.argv[4], house_number=sys.argv[5]
            )
            print("")
            print("========================================================")
            print("Address ID: ", address_data.address_id)
            print("Kommune: ", address_data.kommunenavn)
            print("Vejnavn: ", address_data.vejnavn)
            print("Hus nr.: ", address_data.husnr)

        except Exception as err:
            print(err)

    elif sys.argv[1] == "municipalities":
        for row in MUNICIPALITIES_ARRAY:
            print(row.capitalize())

    elif sys.argv[1] == "categories":
        _sorted_names = sorted(NAME_ARRAY)
        for row in _sorted_names:
            print(row)

    elif sys.argv[1] == "pickup_data":
        try:
            data: PickupEvents = await garbage.get_pickup_data(address_id=sys.argv[3])
            if data is not None:
                print("")
                print("========================================================")
                for item in NAME_ARRAY:
                    if data.get(item) is None:
                        continue
                    print(f"{data[item].friendly_name}:")
                    print("  Nøgle: ", item)
                    print("  Gruppe: ", data[item].group)
                    print("  Navn: ", data[item].friendly_name)
                    try:
                        print("  Dato: ", data[item].date.strftime("%d-%m-%Y"))
                    except:  # noqa: E722
                        print("  Dato: ", data[item].date)
                    print("  Beskrivelse: ", data[item].description)
                    print("  Icon: ", data[item].icon)
                    print("  Picture: ", data[item].entity_picture)
                    print("  Sidst Opdateret: ", data[item].last_updated)
                    print("  ======================================================")

                item = "next_pickup"
                print("Mext Pickup:")
                print("  Gruppe: ", data[item].group)
                print("  Navn: ", data[item].friendly_name)
                print("  Dato: ", data[item].date.strftime("%d-%m-%Y"))
                print("  Beskrivelse: ", data[item].description)
                print("  Icon: ", data[item].icon)
                print("  Picture: ", data[item].entity_picture)
                print("  Sidst Opdateret: ", data[item].last_updated)
                print("  ======================================================")

        except AffaldDKNoConnection as err:
            print(err)

    if session is not None:
        await session.close()

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)


asyncio.run(main())
