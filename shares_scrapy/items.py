# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

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
