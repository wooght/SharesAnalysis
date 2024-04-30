# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :w_re.py
@Author     :wooght
@Date       :2024/4/30 15:59
@Content    :正则匹配模块
"""
import re


class CleanData:
    result_string = ''

    def __init__(self, result_string):
        self.result_string = result_string



    def delete_html(self):
        """
        删除HTML标签
        """
        clean = re.compile('<.*?>')
        self.result_string = re.sub(clean, '', self.result_string)


    def to_compress(self):
        """
        删除空格及换行
        """
        new_data = self.result_string.replace(' ', '')
        self.result_string = new_data.replace('\n', '')
