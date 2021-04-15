# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo


class GbParsePipeline:
    def __init__(self):
        self.db = pymongo.MongoClient('mongodb://localhost')['gb_data_mining']

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(item)
        return item
