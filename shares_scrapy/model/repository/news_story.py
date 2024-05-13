# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :news_story.py
@Author     :wooght
@Date       :2024/5/13 17:56
@Content    :新闻仓库
"""
from ..table import *


class NewsStory:
    def __init__(self):
        s = news.select()
        r = connect.execute(s)
        self.news = r.fetchall()

    def all_url(self):
        result_url = [new.url for new in self.news]
        return result_url

news = NewsStory()