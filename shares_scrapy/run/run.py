# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :run.py
@Author     :wooght
@Date       :2024/5/13 22:07
@Content    :多线程启动多个spider
"""

import threading
import subprocess
import signal
import sys

def start_crawler(spider):
    subprocess.Popen('python runspider.py {}'.format(spider), shell=True)
    print(spider, '启动....')

for arg in sys.argv[1:]:
    # sys.argv 获取python 后空格隔开的参数 第0个为当前文档
    start_crawler(arg)

