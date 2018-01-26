# -*- coding: utf-8 -*-
__author__ = 'xujh'

import logging.config
import configparser
from utils import *

baseconfdir = "./config"
loggingconf = "log.config"
config = "auto.ini"

try:
    logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
    logger = logging.getLogger()

    cf = configparser.ConfigParser()
    cf.read(os.path.join(os.getcwd(), baseconfdir, config), encoding='UTF-8')

    # auto_excel = Excel(cf)
    # auto_excel.load_from_txt()


    # wx = Wx(cf)
    # embed()

    ch = Check(cf)

except BaseException as e:
    logger.exception(e)