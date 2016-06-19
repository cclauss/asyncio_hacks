#!/usr/bin/env python3  # MUST be Python3.5 or better

import aiohttp  # if this line fails, do: pip install aiohttp
import asyncio

async def fetch(client):
    async with client.get('http://python.org') as resp:
        assert resp.status == 200
        return await resp.text()

with aiohttp.ClientSession() as client:
    html = asyncio.get_event_loop().run_until_complete(fetch(client))
    print(html)

