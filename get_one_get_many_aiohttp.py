#!/usr/bin/env python3  # MUST be Python 3.5 or later

'''
async def coroutine_function(urls)
    return coroutine

The coroutine will NOT get executed until:
1. another coroutine function does `await coroutine_function(urls)`
2. loop.run_until_complete(coroutine_function(urls)) is called
'''

import asyncio
import aiohttp
# import logging
import warnings

loop = asyncio.get_event_loop()
loop.set_debug(enabled=True)
# logging.basicConfig(level=logging.DEBUG)
warnings.warn('ResourceWarning', ResourceWarning)

urls = ['http://' + x for x in 'apple.com ibm.com python.org pypy.org'.split()]
url = urls[0]


def async_test(func):  # is func a coroutine function or a coroutine?
    '''https://docs.python.org/3/library/asyncio-task.html'''
    fmt = 'iscoroutine: {}\niscoroutinefunction: {}'
    return fmt.format(asyncio.iscoroutine(func),
                      asyncio.iscoroutinefunction(func))


async def async_get_one(session, url):  # is a coroutinefunction
    fmt = "{} async_get_one('{}')"
    print(fmt.format(0, url))
    async with session.get(url) as resp:
        print(1, url, resp.status)
        return await resp.text()  # returns a coroutine
        # return resp.text()

    '''
    return aiohttp.get(url)   # iscoroutine
    coroutine = requests.get(url).text[:100]
    print(fmt.format(1, url))
    print(coroutine)
    print(async_test(coroutine))
    return coroutine  # iscoroutine
    '''

def get_many(session, urls):
    fmt = "{} async_get_many('{} urls')"
    print(fmt.format(0, len(urls)))
    # return [async_get_one(session, url) for url in urls]
    coroutines = [async_get_one(session, url) for url in urls]
    return [loop.run_until_complete(coroutine) for coroutine in coroutines]


async def async_get_many(session, urls):  # is a coroutinefunction
    fmt = "{} async_get_many('{} urls')"
    print(fmt.format(0, len(urls)))
    # return [async_get_one(session, url) for url in urls]
    coroutines = [async_get_one(session, url) for url in urls]
    pages = []
    for i, coroutine in enumerate(coroutines):
        print('awaiting: {}'.format(i))
        pages.append(await coroutine)
        # pages.append(coroutine)
        print('awaited:  {}'.format(i))
        print(type(pages[-1]))
    print(fmt.format(1, len(pages)))
    return pages  # returns a coroutine
    # return ((await async_get_one(url)) for url in urls)  # iscoroutine


print('=' * 200)
loop = asyncio.get_event_loop()
# async_get_many is a coroutine function
print('\n'.join(('async_get_many', async_test(async_get_many))))
# calling async_get_many(urls) returns a coroutine
with aiohttp.ClientSession() as session:
    a = get_many(session, urls)
    # # a = async_get_many(session, urls)
    # # print('\n'.join(('async_get_many(urls)', str(a))))
    # loop.run_until_complete(a) returns the results of execution
    # # a = loop.run_until_complete(a)

'''
print('async_get:')
print(async_test(async_get))  # iscoroutinefunction
print("async_get('{}'):".format(url))
coro = async_get(url)
print(async_test(coro))  # iscoroutine
a = loop.run_until_complete(coro)
'''
# loop.close()
print(async_test(a[0]))  # iscoroutine
# print(a = loop.create_task(async_get(url)))
# print(a = asyncio.ensure_future(async_get(url)))

for page in a:
    print(type(page))
print('Done.')


# print(list([async_get(url) for url in urls]))
# print(list([(yield from async_get(url)) for url in urls]))
# print(urls)
