#!/usr/bin/env python3

import aiohttp
import asyncio
import pprint

URLS = '''http://perl.org
          http://ruby-lang.org
          http://golang.org
          http://python.org'''.split()

async def fetch(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            return url, await response.text()

async def fetch_many(urls):
    '''Execution is asynchronous with each task result returned returned to
       this function as soon as it is ready, in order of speed of execution.'''
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        result_dict = {}
        for task in asyncio.as_completed([fetch(session, url) for url in urls]):
            url, html = await task
            result_dict[url] = html
            print('Usable:', url, html[:80].replace('\n', ' '))
        return result_dict   

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pages_dict = loop.run_until_complete(fetch_many(URLS))
    #pprint.pprint(pages_dict)
