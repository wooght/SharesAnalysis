# -*- coding: utf-8 -*-
from typing import Iterable

import scrapy
from scrapy import Request
from shares_scrapy.common.echo import echo


class MarketsituationSpider(scrapy.Spider):
    name = "Marketsituation"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["https://sina.com.cn"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": None,
            "shares_scrapy.wmiddlewares.Marketmiddleware.Marketmiddleware": 543
        }
    }

    def start_requests(self):
        echo('从这里开始')
        yield Request(url='https://finance.sina.com.cn/realstock/company/sz002594/hisdata_klc2/klc_kl.js?d=2024_4_29', callback=self.parse)

    def parse(self, response, *args, **kwargs):
        print(response.body)
        print(response.url)

