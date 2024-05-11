# -- coding: utf-8 -
import json

import scrapy
from shares_scrapy.model import proxy_sitory

class Proxy89ipSpider(scrapy.Spider):
    name = "proxy_89ip"
    allowed_domains = ["zhimacangku.com"]
    start_urls = ["http://webapi.http.zhimacangku.com/getip?neek=321a408a&num=10&type=2&time=1&pro=0&city=0&yys=0&port=1&pack=0&ts=0&ys=0&cs=0&lb=1&sb=&pb=4&mr=3&regions="]

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
        ips_list = ["{}:{}".format(x['ip'], x['port']) for x in ips['data']]
        # result_str = response.body.decode('utf-8')
        # tmp_list = result_str.split('</script>')
        # tmp_list2 = tmp_list[-1].split('<br>')
        # del tmp_list2[-1]
        # del tmp_list2[0]
        print(ips_list)
        proxy_sitory.add_proxy(ips_list)
        print('获取成功')
        pass
