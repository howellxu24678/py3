# -*- coding: utf-8 -*-
__author__ = 'xujh'

from wxpy import *
import logging.config
import configparser
import os
from wxpy.api.messages import MessageConfig


baseconfdir = "config"
loggingconf = "log.config"
configfile = "wx.ini"

logger = logging.getLogger()


class Wx(object):
    def __init__(self, cf):
        try:
            self._cf = cf
            group_names = cf.get("wx", "group_names").strip().split(",")
            self._focus = cf.get("wx", "focus").strip().split(",")
            self._txt_file_path = cf.get("wx", "txt_file_path").strip()

            self._bot = Bot(cache_path=True, login_callback=Wx.login_call, logout_callback=Wx.logout_call)
            logger.info("所在的群有：%s", self._bot.groups())
            if len(group_names) > 0:
                groups_set = set()
                for g in group_names:
                    groups_set = groups_set.union(set(self._bot.groups().search(g)))
                self._groups_list = list(groups_set)
            else:
                self._groups_list = self._bot.groups()

            self._bot.register()
            logger.info("将要关注的群：%s", self._groups_list)

            self._bot.registered.append(MessageConfig(
                bot=self, func=Wx.focus_msg(), chats=self._groups_list, msg_types=TEXT,
                except_self=False, run_async=True, enabled=True
            ))
        except BaseException as e:
            logger.exception(e)

    @staticmethod
    def login_call():
        logger.info("login_success")

    @staticmethod
    def logout_call():
        logger.info("logout_success")

    @staticmethod
    def focus_msg(msg):
        print(msg)

    # def focus_msg(self):
    # self.registered.append(MessageConfig(
    #     bot=self, func=func, chats=chats, msg_types=msg_types,
    #     except_self=except_self, run_async=run_async, enabled=enabled
    # ))
#     def save(self, msg):
#         s = "发送者：%s 接受时间：%s 内容：%s" % (msg.member, msg.receive_time, msg.text)
#         with open(txt_file_path, 'a', encoding='UTF-8') as fw:
#             fw.write(s)
#             fw.write("\n")
#         logger.info(s)
#
#     def do_reply(msg, text, at_member=False):
#
#         if at_member:
#             if len(msg.chat) > 2 and msg.member.name:
#                 ret = '@{} {}'.format(msg.member.name, text)
#         else:
#             ret = text
#         logger.info("ret:%s", ret)
#         msg.reply(ret)
#
#     @classmethod
#     @._bot.register(groups_list, TEXT, except_self=False)
#     def focus_msg(msg):
#         try:
#             save(msg)
#
#             if len(focus) > 0:
#                 for f in focus:
#                     if f and msg.text.count(f) > 0:
#                         do_reply(msg, "已收到", True)
#         except BaseException as e_:
#             logger.exception(e_)
# def wait_to_quit():
#     print("按回车键结束")
#     if input():
#         exit()
#
#
# def save(msg):
#     s = "发送者：%s 接受时间：%s 内容：%s" % (msg.member, msg.receive_time, msg.text)
#     with open(txt_file_path, 'a', encoding='UTF-8') as fw:
#         fw.write(s)
#         fw.write("\n")
#     logger.info(s)
#
#
# def do_reply(msg, text, at_member=False):
#
#     if at_member:
#         if len(msg.chat) > 2 and msg.member.name:
#             ret = '@{} {}'.format(msg.member.name, text)
#     else:
#         ret = text
#     logger.info("ret:%s", ret)
#     msg.reply(ret)
#
#
# @Bot.register(self._groups_list, TEXT, except_self=False)
# def focus_msg(msg):
#     try:
#         save(msg)
#
#         if len(focus) > 0:
#             for f in focus:
#                 if f and msg.text.count(f) > 0:
#                     do_reply(msg, "已收到", True)
#     except BaseException as e_:
#         logger.exception(e_)

# def login_call():
#     logger.info("login_success")
#
#
# def logout_call():
#     logger.info("logout_success")
#
# try:
#     logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
#     logger = logging.getLogger()
#     cf = configparser.ConfigParser()
#     cf.read(os.path.join(os.getcwd(), baseconfdir, configfile), encoding='UTF-8')
#
#     group_names = cf.get("global", "group_names").strip().split(",")
#     focus = cf.get("global", "focus").strip().split(",")
#     txt_file_path = cf.get("global", "txt_file_path").strip()
#
#     bot = Bot(cache_path=True, login_callback=login_call, logout_callback=logout_call)
#
#     logger.info("所在的群有：%s", bot.groups())
#     if len(group_names) > 0:
#         groups_set = set()
#         for g in group_names:
#             groups_set = groups_set.union(set(bot.groups().search(g)))
#         groups_list = list(groups_set)
#     else:
#         groups_list = bot.groups()
#
#     logger.info("将要关注的群：%s",groups_list)
#
# except BaseException as e:
#     logger.exception(e)
#     wait_to_quit()
#
#
# @bot.register(groups_list, TEXT, except_self=False)
# def focus_msg(msg):
#     try:
#         save(msg)
#
#         if len(focus) > 0:
#             for f in focus:
#                 if f and msg.text.count(f) > 0:
#                     do_reply(msg, "已收到", True)
#     except BaseException as e_:
#         logger.exception(e_)

embed()

'''
文件传输助手发送消息
bot.file_helper.send('test')
发给个人
frd = bot.friends().search('美丽可爱的琳琳')[0]
frd.send('肥琳，测试一下，不要怕')
发给群
gp = bot.groups().search('测试群')[0]
gp.send('测试一下，不要怕')
历史记录
sent_msg = bot.messages.search(sender=bot.self)

消息简单回复，并不会@人
msg.reply("已收到")

注册的消息
bot.registered

'''
