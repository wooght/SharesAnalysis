# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from shares_scrapy.items import AreaItem, Csrcclassify, SharesItem
from shares_scrapy.model import T, areas_story, csrcs_story, shares_story
from shares_scrapy.common.echo import echo


class SharesScrapyPipeline:
    def __init__(self, *args, **kwargs):
        super(SharesScrapyPipeline, self).__init__(*args, **kwargs)
        all_area = areas_story.all_areas()
        self.exists_csrc = csrcs_story.all_csrcs()
        self.exists_area = all_area.keys()
        self.csrc_parent = {}
        self.shares_code = shares_story.all_code()
        echo("engine start ok")

    def open_spider(self, spider):
        echo('spider: '+spider.name+' -->start ok')
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
            if item['code'] in self.shares_code: return item
            i = T.shares.insert()
            r = T.connect.execute(i, dict(item))
        return item

    def close_spider(self, spider):
        echo('spider: '+spider.name + " stop ok")
        T.connect.commit()
        T.connect.close()
