# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :pipelines.py
@Author     :wooght
@Date       :2024/4/26 15:42
@Content    :spider流程控制模块 管道功能, 数据处理
"""
import json

from itemadapter import ItemAdapter
from shares_scrapy.items import AreaItem, Csrcclassify, SharesItem, MarketItem, NewsItem
from shares_scrapy.model import T, areas_story, csrcs_story, shares_story, news_story
from shares_scrapy.common.echo import echo, echo_info


class SharesScrapyPipeline:
    def __init__(self, *args, **kwargs):
        super(SharesScrapyPipeline, self).__init__(*args, **kwargs)
        all_area = areas_story.all_areas()
        self.exists_csrc = csrcs_story.all_csrcs()
        self.exists_area = all_area.keys()
        self.csrc_parent = {}
        self.shares_code = shares_story.all_code()
        echo_info('pipeline', '管道初始化')

    def open_spider(self, spider):
        echo_info('pipeline', spider.name+' -->启动')
        # 筛选顶级行业分类,供次级分类找到父类ID
        for key, value in self.exists_csrc.items():
            if value['parent_id'] == -1:
                self.csrc_parent[key] = value['id']

    def process_item(self, item, spider):
        if isinstance(item, AreaItem):
            """
                存储地域数据
            """
            if item['name'] in self.exists_area:
                return None
            i = T.area.insert()
            r = T.connect.execute(i, dict(item))
        elif isinstance(item, Csrcclassify):
            """
                存储证监会行业
            """
            if item['name'] in self.exists_csrc.keys():
                return None
            if item['parent_id'] in self.csrc_parent.keys():
                item['parent_id'] = self.csrc_parent[item['parent_id']]
            i = T.csrcclassify.insert()
            r = T.connect.execute(i, dict(item))
        elif isinstance(item, SharesItem):
            """
                单个股票基础信息
            """
            if item['code'] in self.shares_code:
                echo_info('重复存在', item['code'])
                return item
            i = T.shares.insert()
            r = T.connect.execute(i, dict(item))
            T.connect.commit()
        elif isinstance(item, MarketItem):
            """
                股票行情日K
            """
            stack_data = json.loads(item['market'])
            insert_data = []
            for row in stack_data:
                row['share_id'] = item['share_id']
                row['code'] = item['code']
                insert_data.append(row)
            i = T.market.insert()
            r = T.connect.execute(i, insert_data)
            T.connect.commit()
            echo_info('pipeline', str(item['code'])+': 保存'+str(len(insert_data))+'天数据')
        elif isinstance(item, NewsItem):
            """
                新闻
            """
            i = T.news.insert()
            r = T.connect.execute(i, dict(item))
            T.connect.commit()

        return item

    def close_spider(self, spider):
        print('spider: '+spider.name + " stop ok")
        T.connect.commit()
        T.connect.close()
