#!/usr/bin/env python3  # MUST be Python 3.5 or later

import aiohttp
import asyncio

async def fetch(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            return await response.text()

if __name__ == '__zmain__':
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        html = loop.run_until_complete(
            fetch(session, 'http://python.org'))
        print(html)

URLS = '''http://python.org
          http://golang.org
          http://perl.org
          http://ruby-lang.org'''.split()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        coroutines = [fetch(session, url) for url in URLS]
        pages = [loop.run_until_complete(coroutine) for coroutine in coroutines]
        for url, page in zip(URLS, pages):
            print('{}:\n{}=\n{:.100}\n'.format(url, '=' * len(url), page))

