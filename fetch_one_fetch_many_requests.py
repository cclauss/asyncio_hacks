#!/usr/bin/env python3  # MUST be Python 3.5 or later

import asyncio
import requests

loop = asyncio.get_event_loop()

URLS = '''http://python.org
          http://golang.org
          http://perl.org
          http://ruby-lang.org'''.split()


async def fetch_one(url):  # iscoroutinefunction
    print('fetch_one({})'.format(url))
    return await loop.run_in_executor(None, requests.get, url)  # iscoroutine


async def fetch_many(urls):  # iscoroutinefunction
    return await asyncio.gather(*[fetch_one(url) for url in urls])


print('=' * 20)
pages = [resp.text for resp in loop.run_until_complete(fetch_many(URLS))]
for url, page in zip(URLS, pages):
    print('{}:\n\t{}\n'.format(url, page[:100].replace('\n', ' ')))
