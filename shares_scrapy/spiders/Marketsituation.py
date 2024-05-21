# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Marketsituation.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :获取历史行情日K
"""

from scrapy import Request, FormRequest
from shares_scrapy.common.echo import echo_info
from shares_scrapy.common.DateTimeMath import WDate
from shares_scrapy.run.GetProxy import GetProxy
from shares_scrapy.items import MarketItem
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str, is_dict
import json

class MarketsituationSpider(RedisSpider):
    name = "Marketsituation"
    redis_key = 'market_urls'
    # allowed_domains = ["sina.com.cn"]
    # start_urls = ["https://sina.com.cn"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": None,
            "shares_scrapy.wmiddlewares.Marketmiddleware.Marketmiddleware": 543
        }
    }
    url_models = 'https://finance.sina.com.cn/realstock/company/{share}/hisdata_klc2/klc_kl.js?d={now_date}'
    now_date = WDate.now_date.replace('-', '_')
    exists_code = GetProxy('exists_code')

    # def start_requests(self):
    #     # @returns requests 0 10
    #     echo_info('start_request', '开始')
    #     all_shares = shares_story.all_shares()
    #     # shares_obj = OneShare()
    #     # share_obj2 = OneShare()
    #     # shares_obj.id = 5343
    #     # shares_obj.code = '600588'
    #     # shares_obj.symbol = 'sh600588'
    #     # share_obj2.id, share_obj2.code, share_obj2.symbol = 5344, '600657', 'sh600657'
    #     # all_shares = [share_obj2, shares_obj]
    #     exists_market = marketes_story.group_code() if marketes_story.group_code() else []
    #     # exists_market = []
    #     for share in all_shares:
    #         if share.code in exists_market: continue
    #         if self.exists_code.add_ip(share.code): continue
    #         yield Request(url=self.url_model.format(share=share.symbol, now_date=self.now_date),
    #                       errback=self.parse_err,
    #                       callback=self.parse,
    #                       meta={'id': share.id, 'code': share.code, 'symbol': share.symbol, 'proxy_again': False})

    def make_request_from_data(self, data):
        """
        重写make_request_form_data,
        :param data: 任务队列(task queue)数据 json->[url->string,meta->dict]
        :return: FormRequest
        :content: 给request添加errback
        """
        formatted_data = bytes_to_str(data, self.redis_encoding)

        if is_dict(formatted_data):
            parameter = json.loads(formatted_data)
        else:
            print('非JSON格式的任务队列')
            return FormRequest(formatted_data, dont_filter=True)

        if parameter.get('url', None) is None:
            print('任务队列无URL')
            return []

        url = parameter.pop("url")
        method = parameter.pop("method").upper() if "method" in parameter else "GET"
        metadata = parameter.pop("meta") if "meta" in parameter else {}
        return FormRequest(url, dont_filter=True, method=method, formdata=parameter, meta=metadata, errback=self.err_parse)


    def parse(self, response, *args, **kwargs):
        """
        处理response
        :param response:
        :param args:
        :param kwargs:
        :return: MarketItem list[share_id->int,code->string,market->list]
        """
        item = MarketItem()
        # stack_data = json.loads(response.body)
        # meta = {'share_id': response.meta['id'], 'code': response.meta['code']}
        item['share_id'] = response.meta['id']
        item['code'] = response.meta['code']
        item['market'] = response.body
        echo_info(item['code'], 'pipeline处理')
        yield item

    def err_parse(self, failure):
        """
        问题response处理
        :param failure:
        :return: Request
        """
        error_name = failure.value.__class__.__name__
        echo_info('response 错误:', error_name)
        request = failure.request
        meta = {'symbol': request.meta['symbol'], 'id': request.meta['id'], 'code': request.meta['code'],
                'proxy_again': True}
        yield Request(url=request.url, callback=self.parse, errback=self.err_parse, meta=meta, dont_filter=True)
