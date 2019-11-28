# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_db = client['jobparser']
        
    def process_item(self, item, spider):
        if spider.name == 'hhru':
            try:
                item['min_salary'] = int(item['min_salary'])
                item['max_salary'] = int(item['max_salary'])
            except:
                pass
        collection = self.mongo_db[spider.name]
        collection.insert_one(item)
        return item
