import asyncio


async def start_scanner():
    while True:
        print("Scanner running... checking market")

        # Strategy check will be added here later

        await asyncio.sleep(300)
