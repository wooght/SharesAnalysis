# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from shares_scrapy.items import AreaItem, Csrcclassify
from shares_scrapy.module import T, areas
from shares_scrapy.common.echo import echo


class SharesScrapyPipeline:
    def __init__(self, *args, **kwargs):
        super(SharesScrapyPipeline, self).__init__(*args, **kwargs)
        echo("数据提取成功")

    def open_spider(self, spider):
        echo(spider.name+'-->start ok')
        all_area = areas.all()
        self.exists_area = all_area.keys()

    def process_item(self, item, spider):
        if isinstance(item, AreaItem):
            """
                存储地域数据
            """
            if item['name'] in self.exists_area:
                return None
            i = T.area.insert()
            r = T.connect.execute(i, dict(item))
        return item

    def close_spider(self, spider):
        echo(spider.name + "stop ok")
        T.connect.commit()
        T.connect.close()
