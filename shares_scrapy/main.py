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
from celery import Celery
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
backend = 'redis://192.168.101.103:6379/0'
broker = 'redis://192.168.101.103:6379/1'
spider_c = Celery('spider_c', broker=broker, backend=backend)

process = CrawlerProcess(get_project_settings())
# runner = CrawlerRunner(get_project_settings())
@spider_c.task
def get_ips():
    # process.crawl('proxy_89ip')
    # process.start()
    execute(['scrapy', 'crawl', 'proxy_89ip'])