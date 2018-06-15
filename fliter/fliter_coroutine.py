# -*- coding: utf-8 -*-
__author__ = 'xujh'
#多进程实现，但是sqlite只支持一写多读，所以多进行写到某个时刻会报 database is locked

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
db_conn = 'sqlite:///test_cor.db'

log_path = os.path.join(os.getcwd(), 'log')
if not os.path.isdir(log_path):
    os.mkdir(log_path)

logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
logger = logging.getLogger()


def async_get_k_data(_future, _code):
    try:
        logger.info("code:%s", _code)
        #df = ts.get_k_data(_code, start=start_date)
        df = pd.DataFrame()
        _future.set_result(df)
    except BaseException as e:
        logger.exception(e)

async def async_to_sql(_df, _table_name, _engine):
    try:
        if _df is None or len(_df) < 1:
            return
        logger.info("code:%s", _df.index.tolist()[0][0])
        _df.to_sql(_table_name, _engine, if_exists='append')
    except BaseException as e:
        logger.exception(e)


async def async_op_df_k1d(_df_k1d):
    try:
        if _df_k1d is None or len(_df_k1d) < 1:
            return

        code = _df_k1d['code']
        logger.info("code:%s", code.tolist()[0])
        _df_k1d.drop(['code'], 1, inplace=True)
        _df_k1d.insert(0, 'code', code)

        _df_k1d['changeperc'] = round((_df_k1d['close'] - _df_k1d['close'].shift(1)) / _df_k1d['close'].shift(1) * 100, 2)
        # _df_k1d.reset_index(inplace=True)
        _df_k1d.drop(_df_k1d.index.tolist()[0], inplace=True)
        _df_k1d.set_index(['code', 'date'], inplace=True)
        return _df_k1d

    except BaseException as e:
        logger.exception(e)


async def getk1d_to_db(_engine, _code):
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    future._loop.call_soon(async_get_k_data, future, _code)

    df_k1d = await future
    await async_op_df_k1d(df_k1d)
    await async_to_sql(df_k1d, 'k1d', _engine)



def run():
    try:
        engine = create_engine(db_conn)

        code_list = ts.get_stock_basics().index.tolist()
        #code_list = ['000001', '600000', '002325']
        logger.info("code_list:%s", code_list)

        loop = asyncio.get_event_loop()
        tasks = [getk1d_to_db(engine, code) for code in code_list]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    except BaseException as e:
        logger.exception(e)

if __name__ == '__main__':
    run()