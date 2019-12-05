# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

def get_int_value(value):
    return int(''.join(i for i in value[0] if i.isdigit()))
    

class YoulavtoItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(output_processor=get_int_value)
    mileage = scrapy.Field(output_processor=get_int_value)
    color = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=get_int_value)
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
