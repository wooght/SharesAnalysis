# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Historysituation.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :历史行情爬取 代理,不用webdriver
"""
import scrapy
from scrapy import Request
from shares_scrapy.common.DateTimeMath import WDate
from shares_scrapy.common.w_re import CleanData
from shares_scrapy.run.GetProxy import GetProxy
from shares_scrapy.model import shares_story, marketes_story
from shares_scrapy.items import MarketItem
import execjs, json


class HistorysituationSpider(scrapy.Spider):
    name = "Historysituation"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["https://sina.com.cn"]
    url_models = 'https://finance.sina.com.cn/realstock/company/{share}/hisdata_klc2/klc_kl.js?d={now_date}'
    now_date = WDate.now_date.replace('-', '_')
    with open(r'E:\wooght-server\scripy_wooght\shares_scrapy\shares_scrapy\wmiddlewares\js\xh5_s_klc_d.js') as f:
        js_code = f.read()
    xh5js = execjs.compile(js_code)
    exists_code = GetProxy('exists_code')

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": None,
            "shares_scrapy.wmiddlewares.Marketmiddleware.Marketmiddleware": None,
            "shares_scrapy.wmiddlewares.Proxymiddleware.ProxyMiddleware": 400
        }
    }

    def start_requests(self):
        all_shares = shares_story.all_shares()
        exists_market = marketes_story.group_code() if marketes_story.group_code() else []
        for share in all_shares:
            if share.code in exists_market: continue                # 已经存在数据库中
            if self.exists_code.add_ip(share.code) > 0: continue    # 已经存在redis中
            yield Request(url=self.url_models.format(share=share.symbol, now_date=self.now_date), callback=self.parse,
                          errback=self.err_parse,
                          meta={'code': share.code, 'symbol': share.symbol, 'proxy_status': 1, 'id': share.id})

    def parse(self, response, *args):
        item = MarketItem()
        print('成功到parse')
        compress_data = CleanData(response.body.decode('utf-8'))
        compress_data.delete_html()
        compress_data.to_compress()
        just_data = compress_data.result_string.split('"')[1]
        result = self.xh5js.call('xh5_S_KLC_D', just_data)
        markets = []
        for row in result:
            if 'prevclose' in row.keys(): del row['prevclose']
            row['date'] = row['date'].split('T')[0]
            markets.append({key: value for key, value in row.items()})
        item['market'] = json.dumps(markets)
        item['share_id'] = response.meta['id']
        item['code'] = response.meta['code']
        yield item

    def err_parse(self, failure):
        print(failure.value.__class__.__name__)
        request = failure.request
        yield Request(url=self.url_models.format(share=request.meta['symbol'], now_date=self.now_date),
                      callback=self.parse, errback=self.err_parse,
                      meta={'code': request.meta['code'], 'symbol': request.meta['symbol'],
                            'proxy_status': 2, 'id': request.meta['id']})
