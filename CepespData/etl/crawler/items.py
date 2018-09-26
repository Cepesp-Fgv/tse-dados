import os
import re

import scrapy


class TSEFileItem(scrapy.Item):
    file = scrapy.Field()
    path = scrapy.Field()
    year = scrapy.Field()
    name = scrapy.Field()

    file_urls = scrapy.Field()
    files = scrapy.Field()

    @classmethod
    def create(cls, href):
        item = cls()
        item['file'] = href
        item['name'] = os.path.split(href)[-1]
        item['path'] = '/'.join(os.path.split(href)[-4:-1])

        year = re.search('(19[0-8][0-9]|199[0-9]|20[0-8][0-9]|209[0-9])', item['file'])
        if year:
            item['year'] = int(year.group(0))
        else:
            item['year'] = 0

        item['file_urls'] = [href]

        return item

