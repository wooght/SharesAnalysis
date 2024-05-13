# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :runspider.py
@Author     :wooght
@Date       :2024/5/13 22:11
@Content    :启动spider
"""
import sys
from scrapy.cmdline import execute
execute(['scrapy', 'crawl', sys.argv[1]])
