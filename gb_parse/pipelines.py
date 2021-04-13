# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

class GbParsePipeline:
    def process_item(self, item, spider):
        collection = pymongo.MongoClient('mongodb://localhost')['gb_data_mining']['autoyoula']
        collection.insert_one(item)
        return item
