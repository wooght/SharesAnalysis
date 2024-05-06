# -- coding: utf-8 -
import json

import scrapy
from shares_scrapy.model import proxy_sitory

class Proxy89ipSpider(scrapy.Spider):
    name = "proxy_89ip"
    allowed_domains = ["89ip.cn"]
    start_urls = ["http://gev.qydailiip.com/api/?apikey=eb8381122db11006383b3f9d3e3fbe848581ff3c&num=60&type=json&line=win&proxy_type=secret&end_time="]

    # spider 内部修改默认设置
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
        'DOWNLOADER_MIDDLEWARES' : {
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": None,
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        result_rows = proxy_sitory.delete_ips()
        print('删除原始ip {}个'.format(result_rows))

    def parse(self, response, *args, **kwargs):
        ips = json.loads(response.body)
        print(ips)
        # result_str = response.body.decode('utf-8')
        # tmp_list = result_str.split('</script>')
        # tmp_list2 = tmp_list[-1].split('<br>')
        # del tmp_list2[-1]
        # del tmp_list2[0]
        proxy_sitory.add_proxy(ips)
        print('获取成功')
        pass
