# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :run_main.py
@Author     :wooght
@Date       :2024/5/11 21:45
@Content    :
"""

from shares_scrapy.run.mount import get_ips
result = get_ips.delay()
print('id{}'.format(result.id))