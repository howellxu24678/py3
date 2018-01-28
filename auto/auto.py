# -*- coding: utf-8 -*-
__author__ = 'xujh'

import logging.config
import configparser
#from utils import *
import utils
import os

baseconfdir = "./config"
loggingconf = "log.config"
config = "auto.ini"

logger = logging.getLogger()

try:
    logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
    logger = logging.getLogger()

    cf = configparser.ConfigParser()
    cf.read(os.path.join(os.getcwd(), baseconfdir, config), encoding='UTF-8')

    # auto_excel = Excel(cf)
    # auto_excel.load_from_txt()


    # wx = Wx(cf)
    # embed()

    ch = utils.Check(cf)
    excel = utils.Excel(cf, ch)
    excel.upsert_by_line("【审核结果】借款人[张三]。合同金额[1200]元，到账金额[1000]元，期限[10]天，借款日期[2018/01/16]，还款日期[2018/01/26]，到期还款金额[1200]元，逾期管理费[30]元/天，随时可以提前还款，提前还款不收取违约金。")
    excel.upsert_by_line("【还款】[2018.01.19]收到[张三]还款[1500]元。")
    excel.upsert_by_line("【续期】[2018.01.17]收到[张三]续期[200]元，还款日期更改为[2018.02.06]。")
    excel.save()
    #title, values, rtn_str = ch.get_title_values("【审核结果】借款人[张三]。合同金额[1200]元，到账金额[1000]元，期限[10]天，借款日期[2018/01/16]，还款日期[2018/01/26]，到期还款金额[1200]元，逾期管理费[30]元/天，随时可以提前还款，提前还款不收取违约金。")
    #logger.info("title:%s, values:%s, rtn_str:%s", title, values, rtn_str)

except BaseException as e:
    logger.exception(e)