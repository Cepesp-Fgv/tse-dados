import os
import re

import scrapy


def extract_year(url):
    reg = r'(19[0-8][0-9]|199[0-9]|20[0-8][0-9]|209[0-9])'
    return int(re.search(reg, url).group(0))


def extract_uf(url):
    reg = r'(BR|ZZ|VT|AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)'
    return re.search(reg, url).group(0)


def extract_database(url):
    reg = r'(votosecao|votacao_secao|cand|legenda)'
    match = re.search(reg, url).group(0)
    if match == 'votacao_secao' or match == 'votosecao':
        return 'votos'
    elif match == 'cand':
        return 'candidatos'
    elif match == 'legenda':
        return 'legendas'
    else:
        return None


def extract_reg(url):
    reg = r'(uf|meso|micro|munzona|zona|mun|votsec)'
    return re.search(reg, url).group(0)


class SourceFileItem(scrapy.Item):
    path = scrapy.Field()
    name = scrapy.Field()
    database = scrapy.Field()
    year = scrapy.Field()
    uf = scrapy.Field()
    president = scrapy.Field()

    @classmethod
    def create(cls, file_path):
        item = cls()
        item['path'] = file_path
        item['name'] = os.path.split(file_path)[-1]
        item['database'] = extract_database(item['name'])
        item['year'] = extract_year(item['name'])
        item['president'] = "presidente" in item['name']

        if item['database'] == 'votos':
            item['uf'] = extract_uf(item['name'])

        return item


class TSEFileItem(scrapy.Item):
    path = scrapy.Field()
    name = scrapy.Field()
    table = scrapy.Field()
    year = scrapy.Field()
    uf = scrapy.Field()

    @classmethod
    def create(cls, file_path):
        item = cls()
        item['path'] = file_path
        item['name'] = os.path.split(file_path)[-1]
        item['year'] = extract_year(item['name'])

        if item['name'].startswith('vot'):
            item['uf'] = extract_uf(item['name'])
            item['table'] = "votos"

        elif item['name'].startswith("cand"):
            item['table'] = "candidatos"

        elif item['name'].startswith("leg"):
            item['table'] = "legendas"

        return item
