# -*- coding: utf-8 -*-
__author__ = 'xujh'
#多进程实现，但是sqlite只支持一写多读，所以多进行写到某个时刻会报 database is locked

import os
import logging.config
from sqlalchemy import create_engine
import tushare as ts
import multiprocessing



def getk1d_to_sql(_code):
    logger.info("code:%s", _code)

    df_k1d = ts.get_k_data(_code, start=start_date)
    if len(df_k1d) < 1:
        return

    code = df_k1d['code']
    df_k1d.drop(['code'], 1, inplace=True)
    df_k1d.insert(0, 'code', code)

    df_k1d['changeperc'] = round((df_k1d['close'] - df_k1d['close'].shift(1)) / df_k1d['close'].shift(1) * 100, 2)
    # _df.reset_index(inplace=True)
    df_k1d.drop(df_k1d.index.tolist()[0], inplace=True)
    df_k1d.set_index(['code', 'date'], inplace=True)
    # _df.drop(['index'], inplace=True)
    df_k1d.to_sql('k1d', engine, if_exists='append')


def init():
    global start_date
    start_date = '2014-12-31'
    global baseconfdir
    baseconfdir = "config"
    global loggingconf
    loggingconf = "logging.config"
    global db_conn
    db_conn = 'sqlite:///test_multi.db'

    log_path = os.path.join(os.getcwd(), 'log')
    if not os.path.isdir(log_path):
        os.mkdir(log_path)

    logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
    global logger
    logger = logging.getLogger()

    global engine
    engine = create_engine(db_conn)

    # global code_list
    # code_list = ts.get_stock_basics().index.tolist()
    # logger.info("code_list:%s", code_list)


# def save_single():
#     for code in code_list:
#         try:
#
#             getk1d_to_sql(engine, df_k1d, 'k1d')
#         except BaseException as e:
#             logger.exception(e)

def save_multi():
    try:
        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count, initializer=init)
        code_list = ts.get_stock_basics().index.tolist()
        #logger.info("code_list:%s", code_list)
        pool.map(getk1d_to_sql, code_list)

        # global logger
        # logger.info("Started processes")
        #pool.terminate()
        pool.close()
        pool.join()
        # logger.info("Subprocess done.")

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