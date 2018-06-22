# -*- coding: utf-8 -*-
__author__ = 'xujh'
import os
import logging.config
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd

start_date = '2014-12-31'
baseconfdir = "config"
loggingconf = "logging.config"
db_conn = 'sqlite:///test2.db'

log_path = os.path.join(os.getcwd(), 'log')
if not os.path.isdir(log_path):
    os.mkdir(log_path)

logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
logger = logging.getLogger()

def op_df(_df):
    if len(_df) < 1:
        return

    code = _df['code']
    logger.info("code:%s", code.tolist()[0])

    _df.drop(['code'], 1, inplace=True)
    _df.insert(0, 'code', code)

    _df['changeperc'] = round((_df['close'] - _df['close'].shift(1)) / _df['close'].shift(1) * 100, 2)
    _df.drop(_df.index.tolist()[0], inplace=True)
    _df.set_index(['code', 'date'], inplace=True)
    return _df


def run():
    try:
        df_bas = ts.get_stock_basics()
        code_list = df_bas.index.tolist()
        #code_list = ['000001', '002325', '600000']
        logger.info("code_list:len:%s, detail:%s", len(code_list), code_list)

        df_k1d = pd.concat([op_df(ts.get_k_data(code, start=start_date)) for code in code_list])
        logger.info("df_k1d:%s", df_k1d)

        if len(df_k1d) < 1:
            return

        engine = create_engine(db_conn, echo=True)
        df_k1d.to_sql('k1d', engine, if_exists='append')

    except BaseException as e:
        logger.exception(e)

if __name__ == '__main__':
    run()
