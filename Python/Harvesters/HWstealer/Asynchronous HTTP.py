import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:

        for i in range(0, 9999):

            url = "http://pp.iis.p.lodz.pl/reports/subsp/452-2905/215730-a60b/19"

            x = str(i)
            while len(x) < 4:
                x = '0' + x
            url = url + x + "/index.html"

            if i % 50 == 0:
                print(i)

            async with session.get(url) as resp:
                if resp.status != 404:
                    print(url)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
