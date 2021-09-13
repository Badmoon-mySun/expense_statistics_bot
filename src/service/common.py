import aiohttp


async def _is_url_ok(url):
    try:
       async with aiohttp.ClientSession() as session:
           async with session.get(url) as resp:
               return resp.status == 200
    except:
        return False