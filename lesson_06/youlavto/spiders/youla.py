# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['youla.ru']
    start_urls = ['https://auto.youla.ru/stariy-oskol/cars/used/']

    def parse(self, response):
        if response.status == 200:
            next_page = response.xpath('//a[contains(@class, "Paginator_button__u1e7D")]/@href')[-1].extract()
            try:
                pass #yield response.follow(next_page, callback=self.parse)
            except:
                pass
            ads_links = response.xpath('//a[contains(@class, "SerpSnippet_name")]/@href').extract()
            for link in ads_links:
                yield response.follow(link, callback=self.avto_parse)
                
    def avto_parse(self, response):
        if response.status == 200:
            title = response.xpath('//div[@data-target="advert-info-mileage"]/text()').extract_first()
            print(title)
#            loader = ItemLoader(item=JobparserItem(), response=response)
 #           loader.add_xpath('title', '//div[@data-target="advert-title"]/text()')
  #          loader.add_xpath('year', '//div[@data-target="advert-info-year"]/a/text()')
   #         loader.add_xpath('mileage', '//meta[@itemprop="maxValue"]/@content')
    #        loader.add_xpath('color', '//meta[@itemprop="currency"]/@content')
     #       loader.add_value('price', 'hh.ru')
      #      loader.add_value('link', response.url)
       #     yield loader.load_item()            