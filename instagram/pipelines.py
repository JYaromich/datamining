# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

from instagram.items import TagInstagramItem, PostInstagramItem


class SaveMongoPipeline:
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


class SaveImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, PostInstagramItem):
            if item['data']['media'].get('image_versions2'):
                print(item['data']['media']['image_versions2']['candidates'][0]['url'])
                yield scrapy.Request(item['data']['media']['image_versions2']['candidates'][0]['url'])
            if item['data']['media'].get('carousel_media'):
                for itm in item['data']['media']['carousel_media']:
                    yield scrapy.Request(itm['image_versions2']['candidates'][0]['url'])



    def item_completed(self, results, item, info):
        if 'photos' in item:
            item['photos'] = [itm[1] for itm in results]
        return item
