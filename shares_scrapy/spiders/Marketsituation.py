# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Marketsituation.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :获取历史行情日K
"""
from typing import Iterable

import scrapy
from scrapy import Request
from shares_scrapy.common.echo import echo, echo_info
import json
from shares_scrapy.model import T, shares_story, marketes_story
from shares_scrapy.common.DateTimeMath import WDate
from shares_scrapy.items import MarketItem

class OneShare:
    id = 0
    code = 0
    symbol = 0

class MarketsituationSpider(scrapy.Spider):
    name = "Marketsituation"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["https://sina.com.cn"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": None,
            "shares_scrapy.wmiddlewares.Marketmiddleware.Marketmiddleware": 543
        }
    }
    url_models = 'https://finance.sina.com.cn/realstock/company/{share}/hisdata_klc2/klc_kl.js?d={now_date}'
    now_date = WDate.now_date.replace('-', '_')

    def start_requests(self):
        # @returns requests 0 10
        echo_info('start_request', '开始')
        all_shares = shares_story.all_shares()
        # shares_obj = OneShare()
        # share_obj2 = OneShare()
        # shares_obj.id = 5343
        # shares_obj.code = '600588'
        # shares_obj.symbol = 'sh600588'
        # share_obj2.id, share_obj2.code, share_obj2.symbol = 5344, '600657', 'sh600657'
        # all_shares = [share_obj2, shares_obj]
        exists_market = marketes_story.group_code() if marketes_story.group_code() else []
        # exists_market = []
        print(exists_market)
        for share in all_shares:
            if share.code in exists_market: continue
            yield Request(url=self.url_models.format(share=share.symbol, now_date=self.now_date),
                          errback=self.parse_err,
                          callback=self.parse,
                          meta={'id': share.id, 'code': share.code, 'symbol': share.symbol, 'proxy_again': False})

    def parse(self, response, *args, **kwargs):
        item = MarketItem()
        # stack_data = json.loads(response.body)
        # meta = {'share_id': response.meta['id'], 'code': response.meta['code']}
        item['share_id'] = response.meta['id']
        item['code'] = response.meta['code']
        item['market'] = response.body
        # echo(meta['code'], len(stack_data))
        # for stack in stack_data:
        #     item['share_id'] = meta['share_id']
        #     item['code'] = meta['code']
        #     for key, value in stack.items():
        #         item[key] = value
        echo_info(item['code'], 'pipeline处理')
        yield item

    def parse_err(self, failure):
        error_name = failure.value.__class__.__name__
        echo_info('response 错误:', error_name)
        request = failure.request
        meta = {'symbol': request.meta['symbol'], 'id': request.meta['id'], 'code': request.meta['code'],
                'proxy_again': True}
        yield Request(url=request.url, callback=self.parse, errback=self.parse_err, meta=meta)
