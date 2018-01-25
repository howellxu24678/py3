# -*- coding: utf-8 -*-
__author__ = 'xujh'

from utils import *

baseconfdir = "./config"
loggingconf = "log.config"
config = "auto.ini"

try:
    print(os.getcwd())
    logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
    logger = logging.getLogger()

    cf = configparser.ConfigParser()
    cf.read(os.path.join(os.getcwd(), baseconfdir, config), encoding='UTF-8')

    auto_excel = AutoExcel(cf)
    auto_excel.do()
except BaseException as e:
    logger.exception(e)