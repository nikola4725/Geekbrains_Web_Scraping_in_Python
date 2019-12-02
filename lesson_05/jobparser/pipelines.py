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
        item = dict(item)
        if spider.name == 'hhru':
            try:
                item['min_salary'] = int(item['min_salary'])
                item['max_salary'] = int(item['max_salary'])
            except:
                pass
        else:  
            if 'оговорённо' in item['salary']:
                item['min_salary'] = None
                item['max_salary'] = None
                item['currency'] = None
            elif '—' in item['salary']:
                x = item['salary'].split('<span>') 
                item['min_salary'] = int(''.join(i for i in x[1] if i.isdigit()))
                item['max_salary'] = int(''.join(i for i in x[3] if i.isdigit()))
                item['currency'] = x[-1][0]   
            elif 'от' in item['salary']:
                x = item['salary'].split('<span>') 
                item['min_salary'] = int(''.join(i for i in x[1] if i.isdigit()))
                item['max_salary'] = None
                item['currency'] = x[-1][0]   
            elif 'до' in item['salary']:
                x = item['salary'].split('<span>') 
                item['min_salary'] = None
                item['max_salary'] = int(''.join(i for i in x[1] if i.isdigit()))
                item['currency'] = x[-1][0]   
            else:
                x = item['salary'].split('<span>') 
                item['min_salary'] = int(''.join(i for i in x[1] if i.isdigit()))
                item['max_salary'] = item['min_salary']
                item['currency'] = x[-1][0]  
        del item['salary']
        collection = self.mongo_db[spider.name]
        collection.insert_one(item)
        return item
