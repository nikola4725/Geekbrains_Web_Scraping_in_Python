# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class YoulavtoPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongodb = client.youla
        
    def process_item(self, item, spider):
        collection = self.mongodb[spider.name]
        collection.insert_one(item)
        return item
    
    
class YoulavtoPhotosPipeline(ImagesPipeline):
    #путь для сохранения фото - images/id документа в базе/имя файла из ссылки.jpg 
    def file_path(self, request, response=None, info=None):
        filename = request.url.split('/')[-1]
        filedir = request.meta['img_dir']
        filepath = filedir + "/" + filename
        return filepath
    
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    request = scrapy.Request(url=img)
                    request.meta['img_dir'] = item['_id']
                    yield request
                except:
                    pass  
                   
    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


