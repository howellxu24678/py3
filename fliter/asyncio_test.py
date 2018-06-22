# -*- coding: utf-8 -*-
__author__ = 'xujh'


#import threading
import asyncio
import random
import time

@asyncio.coroutine
def test():
    #await time.sleep(random.randint(1, 5))

    for i in range(1, 100000):
        yield
        pow(i, i, i)


async def hello():
    print('Hello world!')
    await asyncio.sleep(2)
    print('Hello again!')

async def hello222(_x):
    print('Hello world! %d' % _x)
    result = await somework(_x)
    print('Hello again!222,result:%s %d'%(result, _x))

@asyncio.coroutine
def sleep(delay):
    yield
    time.sleep(1)

async def somework(_x):
    print('start doing job... %d' % _x)
<<<<<<< HEAD
    #await asyncio.sleep(random.randint(1,5))
    await sleep(random.randint(1,5))

=======
    await asyncio.sleep(random.randint(1,5))
    await test()
>>>>>>> e2b8909c6d5c221899310e4e61c002deffa9e77b
    print("hi, I've done the job %d" % _x )
    return("hi, I've done the job %d" % _x)

loop = asyncio.get_event_loop()
tasks = [hello222(x) for x in range(200)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()