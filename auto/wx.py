# -*- coding: utf-8 -*-
__author__ = 'xujh'

from wxpy import *
import logging.config
import configparser
import os

baseconfdir = "config"
loggingconf = "log.config"
configfile = "wx.ini"

def wait_to_quit():
    print("按回车键结束")
    if input():
        exit()

try:
    logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
    logger = logging.getLogger()
    cf = configparser.ConfigParser()
    cf.read(os.path.join(os.getcwd(), baseconfdir, configfile), encoding='UTF-8')

    group_names = cf.get("global", "group_names").strip().split(",")
    focus = cf.get("global", "focus").strip().split(",")
    txt_file_path = cf.get("global", "txt_file_path").strip()

    bot = Bot(cache_path=True)

    groups_set = set()
    for g in group_names:
        groups_set = groups_set.union(set(bot.groups().search(g)))
    groups_list = list(groups_set)

    logger.info("关注的群：%s",groups_list)

except BaseException as e:
    logger.exception(e)
    wait_to_quit()


@bot.register(groups_list, TEXT, except_self=False)
def group_msg(msg):
    for f in focus:
        if msg.text.count(f) > 0:
            s = "发送者：%s 接受时间：%s 内容：%s" % (msg.member, msg.receive_time, msg.text)
            with open(txt_file_path, 'a', encoding='UTF-8') as fw:
                fw.write(s)
                fw.write("\n")
            logger.info(s)

embed()