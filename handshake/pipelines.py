# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo

from handshake.items import FollowingItem, FollowersItem


class SaveToMongoPipeline:
    @staticmethod
    def __update_date_in_mongo(collection, column_name, item):
        document = collection.find_one({'account_name': item['account_name']})
        document[column_name].append(item['user_name'])
        collection.find_one_and_replace(
            {'account_name': item['account_name']},
            document
        )

    def process_item(self, item, spider):
        collection = pymongo.MongoClient('mongodb://localhost')['gb_data_mining'][spider.name]
        if not collection.find_one({'account_name': item['account_name']}):
            collection.insert_one({
                'account_name': item['account_name'],
                'followers': [],
                'following': []
            })

        if isinstance(item, FollowingItem):
            self.__update_date_in_mongo(collection, 'following', item)

        if isinstance(item, FollowersItem):
            self.__update_date_in_mongo(collection, 'followers', item)
        return item

    def close_spider(self, spider):
        db = pymongo.MongoClient('mongodb://localhost')['gb_data_mining']
        instagram_collection = db[spider.name]
        for document in instagram_collection.find():
            db['instagram_graph'].insert_one({
                'account': document['account_name'],
                'vertex': list(set(document['followers']) & set(document['following']))
            })
        instagram_collection.drop()
