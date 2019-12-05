# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from youlavto.items import YoulavtoItem

class YoulaSpider(scrapy.Spider):
    name = 'youlavto'
    allowed_domains = ['youla.ru']
    start_urls = ['https://auto.youla.ru/stariy-oskol/cars/used/']

    def parse(self, response):
        if response.status == 200:
            next_page = response.xpath('//a[contains(@class, "Paginator_button__u1e7D")]/@href')[-1].extract()
            try:
                yield response.follow(next_page, callback=self.parse)
            except:
                pass
            ads_links = response.xpath('//a[contains(@class, "SerpSnippet_name")]/@href').extract()
            for link in ads_links:
                yield response.follow(link, callback=self.avto_parse)
                
    def avto_parse(self, response):
        if response.status == 200:
            loader = ItemLoader(item=YoulavtoItem(), response=response)
            # _id - записываем в базу под id объявления и потом сохраняем фото в соответствующую папку
            loader.add_xpath('_id', '//div[contains(@class,"AdvertCard_pageContent")]/@data-target-id')
            loader.add_xpath('title', '//div[@data-target="advert-title"]/text()')
            loader.add_xpath('year', '//div[@data-target="advert-info-year"]/a/text()')
            loader.add_xpath('mileage', '//div[@data-target="advert-info-mileage"]/text()')
            loader.add_xpath('color', '//div[@data-target="advert-info-color"]/text()')
            loader.add_xpath('price', '//div[@data-target="advert-price"]/text()')
            loader.add_xpath('photos', '//img[@class="PhotoGallery_photoImage__2mHGn"]/@src')
            loader.add_value('link', response.url)
            yield loader.load_item()            