# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response):
        if response.status == 200:
            next_page = response.xpath('//a[contains(@class,"f-test-link-Dalshe")]/@href').extract_first()
            try:
                yield response.follow(next_page, callback=self.parse)
            except:
                pass
            vacancies_list = response.xpath('//a[contains(@class,"icMQ_ _1QIBo")]/@href').extract()
            for link in vacancies_list:
                yield response.follow(link, callback=self.vacancy_parse)
            
    def vacancy_parse(self, response):
        if response.status == 200:
            vac_site = 'sj.ru'
            vac_name = response.xpath('//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]/text()').extract_first()
            vac_link = response.url
            vac_salary = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]').extract_first()
            yield JobparserItem(site=vac_site, name=vac_name, link=vac_link, salary=vac_salary)
