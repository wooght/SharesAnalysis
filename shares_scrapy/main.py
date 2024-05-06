# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :main.py
@Author     :wooght
@Date       :2024/4/30 16:56
@Content    :运行入口
"""

from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'Marketsituation'])
