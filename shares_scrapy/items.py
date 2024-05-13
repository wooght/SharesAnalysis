# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :items.py
@Author     :wooght
@Date       :2024/4/26 15:42
@Content    :数据定义,项目模型定义
"""

import scrapy


class SharesScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AreaItem(scrapy.Item):
    """
        地域分类
    """
    id = scrapy.Field()             # 本系统地域ID
    name = scrapy.Field()           # 地域名称
    sina_code = scrapy.Field()      # 新浪系统地域编码


class Csrcclassify(scrapy.Item):
    """
        证监会分类
    """
    id = scrapy.Field()             # 被系统分类ID
    name = scrapy.Field()           # 分类名称
    parent_id = scrapy.Field()      # 父级ID
    sina_code = scrapy.Field()      # 新浪系统分类编码


class SharesItem(scrapy.Item):
    """
        股票详细信息
    """
    id = scrapy.Field()             # 本系统ID
    symbol = scrapy.Field()         # 股票代号
    code = scrapy.Field()           # 股票代码
    name = scrapy.Field()           # 名称
    area_id = scrapy.Field()        # 地域ID
    csrc_id = scrapy.Field()        # 证监会行业ID

    new_price = scrapy.Field()      # 最新价格
    min_price = scrapy.Field()      # 最低价格
    max_price = scrapy.Field()      # 最高价格
    open_price = scrapy.Field()     # 今开价格
    last_price = scrapy.Field()     # 昨天价格
    price_change = scrapy.Field()   # 价格变动
    change_percent = scrapy.Field() # 变动幅度

    buy = scrapy.Field()            # 买入
    sell = scrapy.Field()           # 卖出
    amount = scrapy.Field()         # 成交额
    volume = scrapy.Field()         # 成交量

    mktcap = scrapy.Field()         # 总市值
    nmc = scrapy.Field()            # 流通值
    pb = scrapy.Field()             # 市净率


class MarketItem(scrapy.Item):
    """
        股票行情日K
    """
    # id = scrapy.Field()
    # code = scrapy.Field()
    # share_id = scrapy.Field()
    # high = scrapy.Field()
    # low = scrapy.Field()
    # open = scrapy.Field()
    # close = scrapy.Field()
    # amount = scrapy.Field()
    # volume = scrapy.Field()
    # date = scrapy.Field()
    code = scrapy.Field()
    share_id = scrapy.Field()
    market = scrapy.Field()

class NewsItem(scrapy.Item):
    code = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()