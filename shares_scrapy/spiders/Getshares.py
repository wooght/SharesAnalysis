# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from shares_scrapy.items import SharesItem
from shares_scrapy.common.echo import echo
from shares_scrapy.model import T, areas_story, csrcs_story


class GetSharesSpider(scrapy.Spider):
    name = "get_shares"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["https://vip.stock.finance.sina.com.cn/mkt/"]
    url_model = ('https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData'
                 '?page={}&num=80&sort=symbol&asc=1&node={}&symbol=&_s_r_a=page')
    all_target = {'area': areas_story.all_areas(), 'csrc': csrcs_story.all_csrcs(level=2)}

    def __init__(self, target='area', *args, **kwargs):
        """
        重写构造函数
        :param target:  spider传参数,area指通过地域查询,csrc指通过行业查询
            传参命令:scrapy crawl get_shares -a target=csrc
        :param args:
        :param kwargs:
        """
        super(GetSharesSpider, self).__init__(*args, **kwargs)
        self.target = target
        print(self.all_target[target])

    def parse(self, response, *args, **kwargs):
        """
        访问默认页,组装股票条数查询URL
        :param response:
        :param args:
        :param kwargs:
        :return:
        """
        nums_url = ('https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center'
                    '.getHQNodeStockCount?node={}')
        for row in self.all_target[self.target].values():
            # 组装获取股票数量地址
            now_url = nums_url.format(row['code'])
            yield Request(url=now_url, callback=self.nums_parse, meta={'code': row['code'], 'id': row['id']})

    def nums_parse(self, response):
        """
        获取股票数量,组装获取股票信息地址
        :param response: meta['code'','id'] code:要查询的地域或者行业code,id为对应的本系统id
        :return:
        """
        code = response.meta.get("code")
        target_id = response.meta.get('id')
        pages = int(json.loads(response.body)) // 80
        for page in range(1, pages + 2):
            now_url = self.url_model.format(page, code)
            yield Request(url=now_url, callback=self.get_parse if self.target == 'area' else self.update_parse,
                          meta={'id': target_id})

    def get_parse(self, response):
        """
        通过地域获取每支股票基础信息
        :param response: meta['id'] 为area_id
        :return:
        """
        item = SharesItem()
        data = json.loads(response.body)
        item_keys = item.fields.keys()
        area_id = response.meta.get('id')
        # 数据库与新浪字段一一对应
        one_to_one = {'new_price': 'trade', 'min_price': 'low', 'max_price': 'high', 'open_price': 'open',
                      'last_price': 'settlement', 'price_change': 'pricechange', 'change_percent': 'changepercent'}
        for share in data:
            for key in item_keys:
                if key == 'id' or key == 'csrc_id':
                    continue
                elif key == 'area_id':
                    item[key] = area_id
                elif key in one_to_one.keys():
                    item[key] = share[one_to_one[key]]
                else:
                    item[key] = share[key]

            yield item

    def update_parse(self, response):
        """
        修改股票证监会行业分类
        :param response: meta['id'] 为csrc_id
        :return:
        """
        csrc_id = response.meta.get('id')
        all_data = json.loads(response.body)
        for share in all_data:
            share_update = T.shares.update().where(T.shares.c.name == share['name']).values(csrc_id=csrc_id)
            result = T.connect.execute(share_update)
            print(result.rowcount)

