# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :shares_story.py
@Author     :wooght
@Date       :2024/4/26 18:42
@Content    :股票仓库
"""
from ..table import *


def all_shares():
    s = shares.select()
    r = connect.execute(s)
    all_data = r.fetchall()
    return all_data


def all_code():
    all_data = all_shares()
    codes = []
    for row in all_data:
        codes.append(row.code)
    return codes
