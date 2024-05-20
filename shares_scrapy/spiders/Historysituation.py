# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Historysituation.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :历史行情爬取 代理,不用webdriver
"""
import scrapy
from scrapy import Request, FormRequest
from shares_scrapy.common.DateTimeMath import WDate
from shares_scrapy.common.w_re import CleanData
from shares_scrapy.run.GetProxy import GetProxy
from shares_scrapy.model import shares_story, marketes_story
from shares_scrapy.items import MarketItem
import execjs, json
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str, is_dict


class HistorysituationSpider(RedisSpider):
    name = "Historysituation"
    redis_key = 'market_urls'
    # allowed_domains = ["sina.com.cn"]
    # start_urls = ["https://sina.com.cn"]
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

    def __init__(self, production = False,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.production = production

    def start_requests(self):
        # 生产者模式, 添加要爬取的地址到redis
        if self.production:
            all_shares = shares_story.all_shares()
            exists_market = marketes_story.group_code() if marketes_story.group_code() else []
            for share in all_shares:
                if share.code in exists_market: continue  # 已经存在数据库中
                sadd_nums = self.exists_code.add_ip(share.code)
                if sadd_nums == 0: continue  # 已经存在redis中
                meta_info = {
                    'code': share.code,
                    'symbol': share.symbol,
                    'proxy_status': 1,
                    'id': share.id
                }
                url = self.url_models.format(share=share.symbol, now_date=self.now_date)
                request_json = json.dumps({'url': url, 'meta':meta_info, 'method': 'GET'})
                self.server.lpush(self.redis_key, request_json)
                print('共{}个request, 本次push request url {}'.format(self.server.scard, url))
        else:
            return self.next_requests()


    def make_request_from_data(self, data):
        """
        重写make_request_form_data, 上一步操作为next_request获取到redis队列数据
        :param data: 任务队列数据
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
                      callback=self.parse, errback=self.err_parse, dont_filter=True,
                      meta={'code': request.meta['code'], 'symbol': request.meta['symbol'],
                            'proxy_status': 2, 'id': request.meta['id']})
