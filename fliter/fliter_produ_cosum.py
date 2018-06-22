# -*- coding: utf-8 -*-
__author__ = 'xujh'

import os
import logging.config
from sqlalchemy import create_engine
import tushare as ts
import threading
import asyncio
import pandas as pd

start_date = '2014-12-31'
#start_date = '2018-06-14'
baseconfdir = "config"
loggingconf = "logging.config"
db_conn = 'sqlite:///test_produ_cosum.db'
producer_num = 2

log_path = os.path.join(os.getcwd(), 'log')
if not os.path.isdir(log_path):
    os.mkdir(log_path)

logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
logger = logging.getLogger()

def async_get_k_data(_future, _code):
    try:
        #logger.info("code:%s", _code)
        #df = ts.get_k_data(_code, start=start_date)
        df = pd.DataFrame({'code':[_code]})
        _future.set_result(df)
    except BaseException as e:
        logger.exception(e)

async def code_puter(queue_in, code_list):
    logger.info("staring")
    for code in code_list:
        logger.info('put code:%s', code)
        await queue_in.put(code)

    for i in range(producer_num):
        await queue_in.put(None)

    logger.info('waiting for queue to empty')
    await queue_in.join()

    logger.info('ending')


async def producer(queue_in, queue_out, _id):
    logger.info('producer:%s starting', _id)
    while True:
        logger.info('producer:%s waiting for item', _id)
        code = await queue_in.get()
        if code is None:
            queue_in.task_done()
            await queue_out.put(None)
            break
        else:
            logger.info('producer:%s produce code:%s', _id, code)
            loop = asyncio.get_event_loop()
            future = loop.create_future()
            future._loop.call_soon(async_get_k_data, future, code)
            queue_in.task_done()
            df_k1d = await future
            await queue_out.put(df_k1d)
    await queue_out.join()
    logger.info('producer:%s ending', _id)

async def consumer(queue_in, _id):
    logger.info('consumer:%s starting',_id)
    while True:
        logger.info('consumer:%s waiting for item', _id)
        e = await queue_in.get()
        if e is None:
            queue_in.task_done()
            await asyncio.sleep(2)
            while not queue_in.empty():
                logger.info("make sure empty")
                await queue_in.get()
            break
        else:
            logger.info('consumer:%s consume code:%s',_id, e['code'][0])
            queue_in.task_done()

    await queue_in.join()
    logger.info('consumer:%s ending',_id)

async def monitor(queue1, queue2):
    i = 0
    while True:
        await asyncio.sleep(1)
        logger.info("queue1:%s, queue2:%s", queue1._queue, queue2._queue)
        logger.info("queue1 len:%s, queue2 len:%s", queue1.qsize, queue2.qsize)

        i += 1
        if i > 5:
            break


def run():
    try:
        # engine = create_engine(db_conn)
        #
        # code_list = ts.get_stock_basics().index.tolist()
        #code_list = ['000001', '600000', '002325']
        code_list = [str(i) for i in range(5)]
        logger.info("code_list:%s", code_list)

        loop = asyncio.get_event_loop()

        queue_code_list = asyncio.Queue()
        queue_df = asyncio.Queue()

        # for code in code_list:
        #     queue_code_list.put(code)


        tasks = [producer(queue_code_list, queue_df, i) for i in range(producer_num)]
        tasks.append(code_puter(queue_code_list, code_list))
        tasks.append(consumer(queue_df, 1))
        tasks.append(monitor(queue_code_list, queue_df))

        loop.run_until_complete(asyncio.wait(tasks))
        #loop.stop()
        #loop.run_until_complete(asyncio.gather(*tasks))

    except BaseException as e:
        logger.exception(e)
    finally:
        loop.close()


if __name__ == '__main__':
    run()


