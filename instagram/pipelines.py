# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from instagram.items import TagInstagramItem, PostInstagramItem


class InstagramPipeline:
    def process_item(self, item, spider):
        if isinstance(item, TagInstagramItem):
            return self._save_tag(item)
        if isinstance(item, PostInstagramItem):
            return self._save_post(item)
        return item

    def _save_tag(self, item):
        collection = pymongo.MongoClient('mongodb://localhost')['instagram_datamining']['tags']
        collection.insert_one(ItemAdapter(item).asdict())
        return item

    def _save_post(self, item):
        collection = pymongo.MongoClient('mongodb://localhost')['instagram_datamining']['posts']
        collection.insert_one(ItemAdapter(item).asdict())
        return item

class SaveImagePipeline:
    #TODO: create class to save post inage
    pass
