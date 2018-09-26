# -*- coding: utf-8 -*-
import scrapy
from etl.crawler.items import TSEFileItem


class TSESpider(scrapy.Spider):

    name = "tse"
    start_urls = ['http://www.tse.jus.br/hotsites/pesquisas-eleitorais/']
    allowed_domains = ['agencia.tse.jus.br', 'www.tse.jus.br']

    def parse(self, response):
        for link in response.css('a::attr(href)'):
            href = link.extract()
            if href.find('.zip') != -1:
                item = TSEFileItem.create(href)
                if self.is_valid(item):
                    yield item
            elif href.find('.html') != -1:
                yield response.follow(link, self.parse)

    def is_valid(self, item):
        for db in self.settings.get('DATABASES'):
            if db not in item['path']:
                return False

        if item['year'] not in self.settings.get('YEARS'):
            return False

        if item['year'] in [1998, 2006, 2010] and 'BR' in item['name']:
            return False

        return True
