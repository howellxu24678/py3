# -*- coding: utf-8 -*-
__author__ = 'xujh'
#打包 pyinstaller -F --upx-dir D:\soft\upx391w -i edit_128px.ico auto.py
import logging.config
import configparser
import os

baseconfdir = "config"
loggingconf = "log.config"
config = "auto.ini"

logger = logging.getLogger()

ch_count = 40

def tips():
    print()
    print("{}".format("-" * ch_count))
    print('1：微信机器人监听并保存消息')
    print('2：批量记录导入到excel表格中')
    print('3：统计')
    print('q：退出')
    print("{}".format("-" * ch_count))
    print()


def wx_config():
    print()
    print("{}".format("#" * ch_count))
    print("将开启微信机器人记录消息")
    print()
    print("关注的群：{}".format(cf.get("wx", "group_names").strip().split(",")))
    print("关注的词组：{}".format(cf.get("wx", "focus_words").strip().split(",")))
    print("写入的文件目录：{}".format(cf.get("wx", "txt_file_path").strip()))
    print("{}".format("#" * ch_count))
    print()


def excel_config():
    print()
    print("{}".format("#" * ch_count))
    print("将开启批量记录导入到excel表格中")
    print()
    print("txt文件目录：{}".format(cf.get("path", "txt_file_path")))
    print("excel文件目录：{}".format(cf.get("path", "xlsx_file_path")))
    print("{}".format("#" * ch_count))
    print()


def confirm():
    cfm = input("确认以上信息无误开始处理？ \n"
                "(如有误请按n并修改相应配置再次选择)[y/n]")

    if cfm == 'y':
        return True
    else:
        return False

try:
    logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
    logger = logging.getLogger()

    cf = configparser.ConfigParser()

    while(True):
        tips()

        choice = input('请输入你的选择：')
        if choice == 'q':
            os._exit(0)

        if not choice.isdigit():
            print("输入必须为数字，请重新输入")
            continue

        choice_int = int(choice)
        if choice_int < 1 or choice_int > 3:
            print("数字范围有误，请重新输入")
            continue

        cf.read(os.path.join(os.getcwd(), baseconfdir, config), encoding='UTF-8')
        #微信自动保存为文本文件
        if choice_int == 1:
            wx_config()

            if confirm():
                from utils.check import Check
                from utils.wx import Wx
                ch = Check(cf)
                wx = Wx(cf, ch)
                wx.embed_()
            else:
                continue

        #记录导入到excel表格中
        elif choice_int == 2:
            excel_config()

            if confirm():
                from utils.check import Check
                from utils.excel import Excel
                ch = Check(cf)
                excel = Excel(cf, ch)
                excel.upsert_from_txt()
            else:
                continue
        #统计
        elif choice_int == 3:
            pass

except BaseException as e:
    logger.exception(e)
