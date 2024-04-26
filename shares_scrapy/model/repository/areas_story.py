# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :areas_story.py
@Author     :wooght
@Date       :2024/4/25 21:15
@Content    :
"""
from ..table import *


def all_areas():
    s = area.select()
    r = connect.execute(s)
    all_area = r.fetchall()
    area_dict = {}
    for row in all_area:
        area_dict[row.name] = {'id': row.id, 'code': row.sina_code}
    return area_dict
