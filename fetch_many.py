import aiohttp
import asyncio

URLS = '''http://python.org
          http://golang.org
          http://perl.org
          http://ruby-lang.org'''.split()

async def fetch(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def fetch_many(urls):
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        return await asyncio.gather(*[fetch(session, url) for url in urls])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pages = loop.run_until_complete(fetch_many(URLS))
    for url, page in zip(URLS, pages):
        print('{}:\n{}=\n{:.100}\n'.format(url, '=' * len(url), page))

