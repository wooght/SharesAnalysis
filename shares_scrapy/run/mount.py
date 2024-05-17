# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :mount.py
@Author     :wooght
@Date       :2024/4/30 16:56
@Content    :挂载 异步运行代理爬虫
"""
from scrapy.cmdline import execute
import os
import sys
from celery import Celery
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
import multiprocessing
import signal

# signal.signal(signal.SIGCHLD, signal.SIG_IGN)   # 防止僵尸进程
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
backend = 'redis://192.168.101.103:6379/0'
broker = 'redis://192.168.101.103:6379/1'
spider_c = Celery('main', broker=broker, backend=backend, BROKER_CONNECTION_RETRY_ON_STARTUP=True)

def run_spider(queue):
    process = CrawlerProcess(get_project_settings())
    process.crawl('proxy_89ip')
    process.start(stop_after_crawl=True)        # stop_after_crawl 是否在crawler完成之后,停止twsited的reactor


@spider_c.task
def get_ips():
    # execute(['scrapy', 'crawl', 'proxy_89ip'])
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=run_spider, args=(queue, ))
    p.start()
    p.join()