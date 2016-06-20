#!/usr/bin/env python3  # MUST be Python 3.5 or later

import asyncio
import sys

'''
Execute a list of tasks and get their results using asyncio.

Using using various methods determine if:
1. Execution is synchronous (serial) or asynchronous
2. Results are returned as completed or when all task are completed
3. Results are returned in an ordered list or an unordered list
'''


async def factorial(name, number):
    '''Unoptimized task function that is slow on purpose.'''
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        await asyncio.sleep(1)  # slow on purpose!
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))
    return name, f


# pros: None.
# cons: Takes no advantage from asyncio, Removing asyncio simplifies everything
async def get_results_awaited(tasks):  # cons: takes no advantage from asyncio
    '''Execution is synchronous (serial) with each task result returned to
       this function as soon as it is ready, in the same order as the tasks.'''
    # return [await task for task in tasks]  # --> SyntaxError
    # return (await task for task in tasks)  # --> SyntaxError
    # SyntaxError: 'await' expressions in comprehensions are not supported
    results = []
    for task in tasks:
        result = await task
        print('Usable:', result)
        results.append(result)
    return results


# pros: simple, asynchronous execution, results are in the same order as tasks
# cons: waits for ALL tasks complete
async def get_results_gathered(tasks):
    '''Execution is asynchronous with all task results returned only
       when all tasks are completed in the same order as the tasks.'''
    return await asyncio.gather(*tasks)  # add * for a list of tasks


# pros: asynchronous execution, each result is returned as soon as it is ready
# cons: results are in a different order than the tasks
async def get_results_as_completed(tasks):
    '''Execution is asynchronous with each task result returned returned to
       this function as soon as it is ready, in order of speed of execution.'''
    results = []
    for fut in asyncio.as_completed(tasks):
        result = await fut
        print('Usable:', result)
        results.append(result)
    return results


def get_tasks():
    return [factorial("A", 4), factorial("B", 3), factorial("C", 2)]
 

def label(s):
    return '\n{}:\n{}='.format(s, '=' * len(s))


loop = asyncio.get_event_loop()

print(label('Modes of asyncio execution... '))

# pros: asynchronous execution, results are in the same order as tasks
# cons: waits for ALL tasks complete, asyncio.gather() is the same but simpler
'''Execution is asynchronous with all task results returned only
   when all tasks are completed in the same order as the tasks.'''
print(label('asyncio.wait(tasks)'))
tasks = [loop.create_task(task) for task in get_tasks()]
results, exceptions = loop.run_until_complete(asyncio.wait(tasks))
print([result.result() for result in results])

print(label('get_results_gathered(tasks)'))
results = loop.run_until_complete(get_results_gathered(get_tasks()))
print(results)

print(label('get_results_awaited(tasks)'))
results = loop.run_until_complete(get_results_awaited(get_tasks()))
print(results)

print(label('get_results_as_completed(tasks)'))
results = loop.run_until_complete(get_results_as_completed(get_tasks()))
print(results)

loop.close()

'''
Output:

Task A: Compute factorial(2)...
Task B: Compute factorial(2)...
Task C: Compute factorial(2)...
Task A: factorial(2) = 2
Task B: Compute factorial(3)...
Task C: Compute factorial(3)...
Task B: factorial(3) = 6
Task C: Compute factorial(4)...
Task C: factorial(4) = 24”

Excerpt From: Python Documentation Authors. “Python 3.5.2rc1 documentation.” iBooks. 
'''
