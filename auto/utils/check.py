# -*- coding: utf-8 -*-
__author__ = 'xujh'

import re

import logging.config
logger = logging.getLogger()


#数据校验
class Check(object):
    def __init__(self, cf):
        self._cf = cf

        #用于提取标题和数据集的正则表达式
        self._title_re = r'{}'.format(self._cf.get("re", "title").strip())
        self._values_re = r'{}'.format(self._cf.get("re", "values").strip())

        # 每个类型的记录对应提取的结果集个数（用于检查记录是否正确）
        self._dict_title_values_count = {}
        for vc in self._cf.options("values_count"):
            self._dict_title_values_count[vc] = self._cf.getint("values_count", vc)

        # 结果集为数值的位置
        self._dict_title_type_pos = {}
        for fp in self._cf.options("num_pos"):
            num_pos_setting = self._cf.get("num_pos", fp).strip()
            d = {}
            for type_list in num_pos_setting.split(';'):
                type_setting = type_list.strip().split(':')
                d[type_setting[0]] = [int(x) for x in type_setting[1].split(',')]
            self._dict_title_type_pos[fp] = d

        # 结果集校验
        self._dict_check = {}
        for ch in self._cf.options("check"):
            self._dict_check[ch] = self._cf.get("check", ch).strip()

    def get_title_values(self, line):
        rtn_str = str()
        # 每一行有且只有一个标题：审核结果/还款/续期
        titles = re.findall(self._title_re, line)
        if len(titles) != 1:
            rtn_str = "记录内容有误，找到的标题个数不为1，记录内容为：%s" % (line)
            logger.error(rtn_str)
            return None, None, rtn_str

        if not titles[0] in self._dict_title_values_count:
            rtn_str = "没能在配置文件找到对应于标题为：%s 的应提取数据个数配置" % (titles[0])
            logger.error(rtn_str)
            return None, None, rtn_str

        # 提取记录中的数据并做检查
        values = re.findall(self._values_re, line)
        if len(values) != self._dict_title_values_count[titles[0]]:
            rtn_str = "在记录中提取到的数据个数：%s 与配置的应提取个数：%s 不一致，判定有误，记录内容：%s" % \
            (len(values), self._dict_title_values_count[titles[0]], line)
            logger.error(rtn_str)
            return None, None, rtn_str

        #数值类型修正
        if titles[0] in self._dict_title_type_pos:
            for k,v in self._dict_title_type_pos[titles[0]].items():
                for pos in v:
                    values[pos] = eval(k + "({})".format(values[pos]))

        if titles[0] in self._dict_check and not eval(self._dict_check[titles[0]]):
            rtn_str = "记录无法通过配置文件对标题：%s的校验，记录内容：%s" % (titles[0], line)
            logger.error(rtn_str)
            return None, None, rtn_str

        return titles[0], values, rtn_str

