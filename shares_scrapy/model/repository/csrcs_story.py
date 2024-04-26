# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :csrcs_story.py
@Author     :wooght
@Date       :2024/4/26 15:42
@Content    :证监会行业仓库
"""

from ..table import *


def all_csrcs(level=0):
    """
    获取全部证监会行业
    :return: [{name:**,id:**,parent_id:**,sine_code:**},...]
    """
    i = csrcclassify.select() if level == 0 else csrcclassify.select().filter(csrcclassify.c.parent_id > 0)
    r = connect.execute(i)
    all_data = r.fetchall()
    result_dict = {}
    for row in all_data:
        result_dict[row.name] = {'name': row.name, 'id': row.id,
                                 'parent_id': row.parent_id, 'code': row.sina_code}
    return result_dict
