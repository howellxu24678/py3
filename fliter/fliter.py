# -*- coding: utf-8 -*-
__author__ = 'xujh'
import os
import logging.config
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import time

start_date = '2014-12-31'
baseconfdir = "config"
loggingconf = "logging.config"
db_conn = 'sqlite:///fliter.db'
engine = create_engine(db_conn, echo=True)

log_path = os.path.join(os.getcwd(), 'log')
if not os.path.isdir(log_path):
    os.mkdir(log_path)

logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
logger = logging.getLogger()

def op_k1d_df(_df):
    if len(_df) < 1:
        return

    code = _df['code']
    logger.info("code:%s", code.tolist()[0])

    #获取到的code列在最后，删掉编排到前面，与date作为主键
    _df.drop(['code'], 1, inplace=True)
    _df.insert(0, 'code', code)

    #当日涨幅
    _df['changeperc'] = round((_df['close'] - _df['close'].shift(1)) / _df['close'].shift(1) * 100, 2)
    #当日振幅
    _df['aplt'] = round((_df['high'] - _df['low']) / _df['close'].shift(1) * 100, 2)
    #删掉第一行(有0值)
    _df.drop(_df.index.tolist()[0], inplace=True)
    #设置索引为code和date
    _df.set_index(['code', 'date'], inplace=True)

    return _df

def update_base():
    df_base = ts.get_stock_basics()
    #每股收益置为两位小数
    df_base['esp'] = df_base['esp'].round(2)
    df_base.to_sql('base', engine, if_exists='replace')

def update_profit():
    cur_year = time.localtime().tm_year
    df_profit = pd.concat([ts.profit_data(cur_year, 'all'), ts.profit_data(cur_year - 1, 'all')])
    df_profit.set_index(['code', 'year'], inplace=True)
    df_profit.to_sql('profit', engine, if_exists='replace')

def save_k1d():
    try:
        df_base = ts.get_stock_basics()
        code_list = df_base.index.tolist()
        #code_list = ['000001']
        logger.info("code_list:len:%s, detail:%s", len(code_list), code_list)

        df_k1d = pd.concat([op_k1d_df(ts.get_k_data(code, start=start_date)) for code in code_list])
        logger.info("df_k1d:%s", df_k1d)

        if len(df_k1d) < 1:
            return

        df_k1d.to_sql('k1d', engine, if_exists='append')

    except BaseException as e:
        logger.exception(e)

def read():
    pd.read_sql('k1d', engine)

if __name__ == '__main__':
    save_k1d()
    update_base()
    update_profit()



'''
import os
os.getcwd()
from sqlalchemy import create_engine
os.chdir(r'E:\pan\work\code\github\py3\fliter')
db_conn = 'sqlite:///test2.db'
engine = create_engine(db_conn, echo=True)

import tushare as ts
import pandas as pd

df_base = ts.get_stock_basics()
df_base.to_sql('base', engine, if_exists='append')

select strftime('%Y-%m-%d', datetime('now','-10 day','start of day'))
select strftime('%Y-%m-%d', datetime('now','-10 day','start of day'))
'''