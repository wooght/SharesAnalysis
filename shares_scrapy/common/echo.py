# -- coding: utf-8 -
"""
@project    :HandBook
@file       :echo.py
@Author     :wooght
@Date       :2024/3/15 18:10
@Content    : 简易输出模块区分
"""
import time
from shares_scrapy.common.DateTimeMath import WDate


def echo(*ss):
    if len(ss) == 1:
        print("=" * 80, '\r\n', ss[0].center(80, " "), '\r\n', "=" * 79, end='\r\n')
    else:
        print("_" * 50)
        for s in ss: print(s)
        print("-" * 30)


def echo_info(self='', ss=''):
    print(WDate.real_time()+" INFO [", self, '] : ', ss)


if __name__ == '__main__':
    echo_info('爬虫', '爬虫启动')
    time.sleep(1)
    echo_info()
