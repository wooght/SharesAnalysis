# -- coding: utf-8 -
import json

import scrapy
from shares_scrapy.model import proxy_sitory
from shares_scrapy.run.GetProxy import GetProxy

class Proxy89ipSpider(scrapy.Spider):
    name = "proxy_89ip"
    allowed_domains = ["zhimacangku.com"]
    start_urls = ["http://webapi.http.zhimacangku.com/getip?neek=321a408a&num=3&type=2&time=1&pro=0&city=0&yys=0&port=1&pack=0&ts=0&ys=0&cs=0&lb=1&sb=&pb=4&mr=3&regions="]

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
    proxy_ip = GetProxy('proxy_ips')

    def parse(self, response, *args, **kwargs):
        ips = json.loads(response.body)
        print(ips)
        ips_list = ["{}:{}".format(x['ip'], x['port']) for x in ips['data']]
        # result_str = response.body.decode('utf-8')
        # tmp_list = result_str.split('</script>')
        # tmp_list2 = tmp_list[-1].split('<br>')
        # del tmp_list2[-1]
        # del tmp_list2[0]
        if len(ips_list) > 0: print('共获取{}条IP'.format(self.proxy_ip.add_ip(ips_list)))
        else: print('获取IP失败')

"""
    白名单接口:
    https://wapi.proxy.linkudp.com/api/save_white?neek=2660780&appkey=aab53e578b4231dde138bb7214301f21&white=您的ip
    获取本机IP地址:
    http://httpbin.org/ip
"""