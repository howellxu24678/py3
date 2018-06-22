# -*- coding: utf-8 -*-
__author__ = 'xujh'

import random
import time
import asyncio
import string
async def producer(queue, _id):
    item = string.ascii_letters
    loop = 0
    while True:
        e = random.choice(item)
        print('product:{} by producer<{}>'.format(e, _id))
        await queue.put(e)
        await asyncio.sleep(random.random())
        loop += 1
        if loop == 20:
            break


async def consumer(queue, _id):
	loop = 0
	while True:
		e = await queue.get()
		print('sonsume:{} by consumer<{}>'.format(e, _id))
		queue.task_done()
		await asyncio.sleep(random.random())
		loop += 1
		if loop == 20:
			break
async def monitor(queue):
	loop = 0
	while True:
		await asyncio.sleep(5)
		print(queue._queue)
		loop += 1
		if loop == 5:
			break
def main():
	queue = asyncio.Queue()
	producer1 = producer(queue, 1)
	producer2 = producer(queue, 2)
	consumer1 = consumer(queue, 1)
	consumer2 = consumer(queue, 2)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.gather(*[producer1, producer2, consumer1, consumer2, monitor(queue)]))
if __name__ == '__main__':
	main()