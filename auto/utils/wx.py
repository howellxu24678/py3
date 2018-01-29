# -*- coding: utf-8 -*-
__author__ = 'xujh'

from wxpy import *
import logging.config

logger = logging.getLogger()


class Wx(object):
    def __init__(self, cf, check):
        try:
            #self._cf = cf
            self._check = check

            group_names = cf.get("wx", "group_names").strip().split(",")
            self._focus_words = cf.get("wx", "focus_words").strip().split(",")
            self._txt_file_path = cf.get("wx", "txt_file_path").strip()


            self._bot = Bot(cache_path=True, login_callback=Wx.login_call, logout_callback=Wx.logout_call)
            all_groups = self._bot.groups()
            logger.debug("所在的群有：%s", all_groups)

            if len(group_names) > 0:
                groups_set = set()
                for g in group_names:
                    groups_set = groups_set.union(set(all_groups.search(g)))
                self._groups_list = list(groups_set)
            else:
                self._groups_list = all_groups

            logger.info("将要关注的群：%s", self._groups_list)

            self.focus_msg = self._bot.register(self._groups_list, TEXT, False)(self.focus_msg)
        except BaseException as e:
            logger.exception(e)

    @staticmethod
    def login_call():
        logger.info("login_success")

    @staticmethod
    def logout_call():
        logger.info("logout_success")

    @staticmethod
    def do_reply(msg, text, at_member=False):

        ret = str()
        if at_member:
            if len(msg.chat) > 2 and msg.member.name:
                ret = '@{} {}'.format(
                    msg.member.raw.get('nick_name') if msg.member.raw.get('nick_name') else msg.member.name,
                    text)
        else:
            ret = text

        logger.info("机器人回复的消息:%s", ret)
        msg.reply(ret)

    def save_to_file(self, msg):
        s = "发送者：%s 接受时间：%s 内容：%s" % (msg.member, msg.receive_time, msg.text)
        with open(self._txt_file_path, 'a', encoding='UTF-8') as fw:
            fw.write(s)
            fw.write("\n")
        logger.info(s)

    def focus_msg(self, msg):
        try:
            # if len(self._focus_words) < 1:
            #     return
            for f in self._focus_words:
                if not f or msg.text.count(f) < 1:
                    return

                title, values, rtn_str = self._check.get_title_values(msg.text)
                if not title or not values:
                    return Wx.do_reply(msg, rtn_str, True)

                Wx.do_reply(msg, "已收到", True)

                self.save_to_file(msg)

        except BaseException as e:
            logger.exception(e)

'''
文件传输助手发送消息
_bot.file_helper.send('test')
发给个人
frd = _bot.friends().search('美丽可爱的琳琳')[0]
frd.send('肥琳，测试一下，不要怕')
发给群
gp = _bot.groups().search('测试群')[0]
gp.send('测试一下，不要怕')
历史记录
sent_msg = _bot.messages.search(sender=_bot.self)

消息简单回复，并不会@人
msg.reply("已收到")

注册的消息
_bot.registered
'''
