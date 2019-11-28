# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        try:
            pass #yield response.follow(next_page, callback=self.parse)
        except:
            pass
        vacancies_list = response.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href').extract()
        for link in vacancies_list:
            yield response.follow(link, callback=self.vacancy_parse)
            
    def vacancy_parse(self, response):
        vac_site = 'hh.ru'
        vac_name = response.xpath('//head/title/text()').extract_first()
        vac_link = response.xpath('//meta[@itemprop="url"]/@content').extract_first()
        vac_currency = response.xpath('//meta[@itemprop="currency"]/@content').extract_first()
        vac_min_salary = response.xpath('//meta[@itemprop="minValue"]/@content').extract_first()
        vac_max_salary = response.xpath('//meta[@itemprop="maxValue"]/@content').extract_first()
        yield JobparserItem(site=vac_site, name=vac_name, link=vac_link, curr=vac_currency, min_salary=vac_min_salary, max_salary=vac_max_salary)
