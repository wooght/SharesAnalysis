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

    @staticmethod
    def del_html_list(list_str):
        r = re.compile('<.*?>')
        result_str = ''
        for s in list_str:
            result_str += re.sub(r, '', CleanData.to_compress_static(s))
        return result_str

    @staticmethod
    def to_compress_static(text):
        text = text.replace(' ', '')
        return text.replace('\n', '')
