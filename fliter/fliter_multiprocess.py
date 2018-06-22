# -*- coding: utf-8 -*-
__author__ = 'xujh'
#多进程实现，但是sqlite只支持一写多读，所以多进行写到某个时刻会报 database is locked

import os
import logging.config
from sqlalchemy import create_engine
import tushare as ts
import multiprocessing
import pandas as pd

start_date = '2014-12-31'
#start_date = '2018-06-19'
baseconfdir = "config"
loggingconf = "logging.config"
db_conn = 'sqlite:///test_multi.db'

log_path = os.path.join(os.getcwd(), 'log')
if not os.path.isdir(log_path):
    os.mkdir(log_path)

logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
logger = logging.getLogger()

def getk1d(_code):
    logger.info("code:%s", _code)
    df_k1d = ts.get_k_data(_code, start=start_date)
    if len(df_k1d) < 1:
        return

    code = df_k1d['code']
    df_k1d.drop(['code'], 1, inplace=True)
    df_k1d.insert(0, 'code', code)

    df_k1d['changeperc'] = round((df_k1d['close'] - df_k1d['close'].shift(1)) / df_k1d['close'].shift(1) * 100, 2)
    df_k1d.drop(df_k1d.index.tolist()[0], inplace=True)
    df_k1d.set_index(['code', 'date'], inplace=True)
    return df_k1d
    #df_k1d.to_sql('k1d', engine, if_exists='append')


def init():
    pass


    # global engine
    # engine = create_engine(db_conn)

    # global code_list
    # code_list = ts.get_stock_basics().index.tolist()
    # logger.info("code_list:%s", code_list)


# def save_single():
#     for code in code_list:
#         try:
#
#             getk1d(engine, df_k1d, 'k1d')
#         except BaseException as e:
#             logger.exception(e)

def save_multi():
    try:
        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=2, initializer=init)
        code_list = ts.get_stock_basics().index.tolist()
        #code_list = [str(i) for i in range(50)]
        #code_list = ['000001', '002325', '600000']
        #logger.info("code_list:%s", code_list)
        df = pd.concat(pool.map(getk1d, code_list))
        logging.info("ret:%s", df)

        engine = create_engine(db_conn)
        df.to_sql('k1d', engine, if_exists='append')

        pool.close()
        pool.join()

    except BaseException as e:
        print(e)




if __name__ == '__main__':
    save_multi()


# _df = ts.get_k_data('002908', start = start_date)
# code = _df['code']
# _df.drop(['code'], 1, inplace=True)
# _df.insert(0, 'code', code)
#
# _df['changeperc'] = (_df['close'] - _df['close'].shift(1)) / _df['close'].shift(1) * 100
# #_df.reset_index(inplace=True)
# _df.drop(_df.index.tolist()[0], inplace=True)
# _df.set_index(['code', 'date'], inplace=True)
# #_df.drop(['index'], inplace=True)
# _df.to_sql('k1d', engine, if_exists='replace')




#df.insert(0, 'date', '2018-06-13')
#if_exists:fail replace append
#df.to_sql('basics', engine, if_exists='replace')
#######

#算涨幅 (df['close'] - df['close'].shift(1)) / df['close'].shift(1) * 100