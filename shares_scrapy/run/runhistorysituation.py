# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :runhistorysituation.py
@Author     :wooght
@Date       :2024/5/13 22:07
@Content    :多线程启动多个spider
"""

import threading
from scrapy.cmdline import execute
import subprocess
import signal
from multiprocessing import Process

# class SpiderThread(threading.Thread):
#     def __init__(self, spider):
#         super().__init__()
#         self.spider = spider
#
#     def run(self):
#         crawler(self.spider)
#
# crawler_pool = {}  # 爬虫池
# threads_pool = []  # 线程池
# def crawler(spider):
#     global scrapy
#     scrapy[spider] = subprocess.Popen(execute(['scrapy', 'crawl', spider]), shell=True)
#     print(spider, scrapy[spider], '开始运行')
#
# spider_list = ['Historysituation', 'Marketsituation']
# for spider in spider_list:
#     threads_pool.append(SpiderThread(spider))
#     threads_pool[-1].start()
#
# while True:
#     mm = input("Runing:")
#     if 'stop' in mm:
#         try:
#             spider = mm.split(',')[1]
#             crawler_pool[spider].send_signal(signal.CTRL_C_EVENT)  # 发送Ctrl+c 命令
#             crawler_pool[spider].kill()
#             print('kelld:', spider)
#         except Exception as e:
#             print(e)
#             print('input agrent....')

def crawl(s):
    execute(['scrapy', 'crawl', s])
spider_list = ['Historysituation', 'Marketsituation']
if __name__ == '__main__':
    spider_pool = []
    for spider in spider_list:
        spider_pool.append(Process(target=crawl, args=(spider,)))
        spider_pool[-1].start()
    for spider in spider_pool:
        spider.join()