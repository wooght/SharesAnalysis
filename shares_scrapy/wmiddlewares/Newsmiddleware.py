# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Newsmiddleware.py
@Author     :wooght
@Date       :2024/5/13 19:30
@Content    :新闻中间件,主要控制随机访问时间
"""
import time
import random
from scrapy.utils.project import get_project_settings

class Newsmiddleware:
    def __init__(self):
        self.delay = get_project_settings().get('RANDOM_DELAY')

    def process_request(self, request, spider):
        print('访问地址:{}'.format(request.url))
        if spider.name == 'news':
            delay = random.randint(1, self.delay)
            print('暂停{}秒'.format(delay))
            time.sleep(delay)

    def process_exception(self, request, exception, spider):
        print('捕获错误:{},url:{}'.format(exception.__class__.__name__, request.url))
        print('错误headers')
        print(request.headers)
        return None