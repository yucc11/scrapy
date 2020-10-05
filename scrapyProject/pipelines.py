# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class ScrapyprojectPipeline:

    def process_item(self, item, spider):
        item['price'] = int(item['price'])
        return item

class MongoDBPipeline:

    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI')
        db_name = spider.settings.get('MONGODB_DB_NAME')
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]


    def process_item(self, item, spider):
        self.insert_product(item)
        return item

    def insert_product(self, item):
        item = dict(item)
        self.db.products.insert_one(item)

    def close_spider(self, spider):
        self.db_client.close()



