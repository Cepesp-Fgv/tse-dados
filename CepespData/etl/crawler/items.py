import os
import re

import scrapy


def extract_year(url):
    reg = r'(19[0-8][0-9]|199[0-9]|20[0-8][0-9]|209[0-9])'
    try:
        return int(re.search(reg, url).group(0))
    except:
        return 0


def extract_uf(url):
    reg = r'(BR|ZZ|VT|AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)'
    try:
        return re.search(reg, url).group(0)
    except:
        return None


def extract_turn(url):
    reg = r'(1t|2t)'
    try:
        return re.search(reg, url).group(0)
    except:
        return None


class TSEFileItem(scrapy.Item):
    file = scrapy.Field()
    path = scrapy.Field()
    year = scrapy.Field()
    name = scrapy.Field()
    uf = scrapy.Field()
    turn = scrapy.Field()

    file_urls = scrapy.Field()
    files = scrapy.Field()

    @classmethod
    def create(cls, href):
        item = cls()
        item['file'] = href
        item['name'] = os.path.split(href)[-1]
        item['path'] = '/'.join(os.path.split(href)[-4:-1])
        item['year'] = extract_year(item['name'])
        if item['year'] == 0:
            item['year'] = extract_year(item['file'])

        item['uf'] = extract_uf(item['name'])
        item['turn'] = extract_turn(item['name'])

        item['file_urls'] = [href]

        return item

