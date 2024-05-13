# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :news.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :股票新闻爬虫
"""
from typing import Iterable

import scrapy
from scrapy import Request
from shares_scrapy import model as T
from shares_scrapy.model.repository import shares_story, news_story
from shares_scrapy.common.w_re import CleanData
from shares_scrapy.items import NewsItem
import random


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["10jqka.com.cn"]
    start_urls = ["https://10jqka.com.cn"]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'DOWNLOADER_MIDDLEWARES': {
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": 543,
            "shares_scrapy.wmiddlewares.Newsmiddleware.Newsmiddleware": 555
        }
    }
    cleandata = CleanData('')
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-Hans-CN;q=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.err_url = []

    def start_requests(self):
        """所有股票code"""
        all_story = shares_story.all_code()
        """已经存在的新闻"""
        self.all_url = news_story.news.all_url()
        url_model = 'https://stockpage.10jqka.com.cn/{}/'
        random.shuffle(all_story)           # 打乱顺序
        for code in all_story:
            yield Request(url=url_model.format(code), callback=self.parse, meta={'code': code})
        # yield Request(url=url_model.format('600101'), callback=self.parse, meta={'code':'600101'})

    def parse(self, response, *args):
        """获取新闻地址列表"""
        urls = response.css('ul.news_list')[0].css('li span a::attr(href)').getall()
        """#xwgg > ul > li:nth-child(1) > span.news_title.fl > a"""
        print(urls)
        for url in urls:
            if url not in self.all_url:
                yield Request(url=url, callback=self.new_parse, meta={'code':response.meta['code']}, errback=self.err_parse)
            else:
                print('已经存在')

    def new_parse(self, response):
        item = NewsItem()
        item['date'] = response.css('#pubtime_baidu::text').get().split(' ')[0]
        item['title'] = response.css('h2.main-title::text').get()
        text_html = response.css('div.main-text')[0].css('p').getall()
        item['text'] = self.cleandata.del_html_list(text_html)
        item['code'] = response.meta['code']
        item['url'] = response.url
        print('to pipeline {},{}'.format(item['title'], item['url']))
        yield item

    def err_parse(self, failure):
        print('错误:{}'.format(failure.value.__class__name))
        print('错误headers')
        request = failure.request
        print(request.headers)
        url = request.url
        if url not in self.err_url:
            self.err_url.append(url)
            yield Request(url=url, callback=self.new_parse, headers=self.header,
                          meta={'code':request.meta['code']}, errback=self.err_parse)
        else:
            print('错误超过1次以上')