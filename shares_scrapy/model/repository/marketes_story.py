# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :marketes_story.py
@Author     :wooght
@Date       :2024/4/30 18:35
@Content    :行情仓库
"""
from ..table import *


def group_code():
    """
    获取已经存在行情的code
    :return: [code,code,...]
    """
    s = select(func.count(Column('id')).label('count'), Column('code')).select_from(market).group_by(market.c.code)
    r = connect.execute(s)
    result_list = []
    for row in r.fetchall():
        result_list.append(row.code)
    return result_list


def share_market(share_id):
    """
    获取某个share的行情
    :param share_id:
    :return: queryObject
    """
    s = market.select().where(market.c.id == share_id)
    r = connect.execute(s)
    return r.fetchall()