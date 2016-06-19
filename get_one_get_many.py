import asyncio
import requests

urls = ['http://' + x for x in 'apple.com ibm.com python.org pypy.org'.split()]
url = urls[0]


def async_test(func):
    '''https://docs.python.org/3/library/asyncio-task.html'''
    fmt = 'iscoroutine: {}\niscoroutinefunction: {}'
    return fmt.format(asyncio.iscoroutine(func),
                      asyncio.iscoroutinefunction(func))


async def async_get_one(url):  # iscoroutinefunction
    return requests.get(url).text[:100]  # iscoroutine


async def async_get_many(urls):  # iscoroutinefunction
    pages = []
    for coroutine in [async_get_one(url) for url in urls]:
        pages.append(await coroutine)
    return pages  # iscoroutine
    # return ((await async_get_one(url)) for url in urls)  # iscoroutine


loop = asyncio.get_event_loop()
print(async_test(async_get_many))
a = async_get_many(urls)
print(async_test(a))
a = loop.run_until_complete(async_get_many(urls))

'''
print('async_get:')
print(async_test(async_get))  # iscoroutinefunction
print("async_get('{}'):".format(url))
coro = async_get(url)
print(async_test(coro))  # iscoroutine
a = loop.run_until_complete(coro)
'''
#loop.close()
print(async_test(a))  # iscoroutine
#print(a = loop.create_task(async_get(url)))
# print(a = asyncio.ensure_future(async_get(url)))

print('\n\n'.join(a))
print('Done.')

    
# print(list([async_get(url) for url in urls]))
# print(list([(yield from async_get(url)) for url in urls]))
# print(urls)