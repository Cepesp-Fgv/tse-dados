import os
import re

import scrapy


def extract_year(url):
    reg = r'(19[0-8][0-9]|199[0-9]|20[0-8][0-9]|209[0-9])'
    try:
        return int(re.search(reg, url).group(0))
    except AttributeError:
        return 0


def extract_uf(url):
    reg = r'(BR|ZZ|VT|AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)'
    return re.search(reg, url.upper()).group(0)


def extract_database(url):
    reg = r'(detalhe|votosecao|votacao_secao|bem_cand|cand|legenda|filiados)'
    try:
        match = re.search(reg, url).group(0)
    except AttributeError:
        match = None

    if match == 'detalhe':
        return 'detalhe'
    elif match == 'votacao_secao' or match == 'votosecao':
        return 'votos'
    elif match == 'bem_cand':
        return 'bem_candidato'
    elif match == 'cand':
        return 'candidatos'
    elif match == 'legenda':
        return 'legendas'
    elif match == 'filiados':
        return 'filiados'
    else:
        return None


def extract_reg(url):
    reg = r'(uf|meso|micro|munzona|zona|mun|votsec)'
    return re.search(reg, url).group(0)


def extract_party(name):
    reg = r'(solidariedade|avante|novo|patri|pode|pc_do_b|prtb|psdb|pstu|psol|pros|rede|dem|mdb|pcb|pco|pdt|phs|pmb' \
          r'|pmn|ppl|pps|prb|psb|psc|psd|psl|ptb|ptc|prp|pv|dc|pr|pp|pt)'
    return re.search(reg, name).group(0)


class SourceFileItem(scrapy.Item):
    path = scrapy.Field()
    name = scrapy.Field()
    database = scrapy.Field()
    year = scrapy.Field()
    uf = scrapy.Field()
    president = scrapy.Field()
    party = scrapy.Field()

    @classmethod
    def create(cls, file_path):
        item = cls()
        item['path'] = file_path
        item['name'] = os.path.split(file_path)[-1]
        item['database'] = extract_database(item['name'])
        item['president'] = "presidente" in item['name']

        if item['database'] != 'filiados':
            item['year'] = extract_year(item['name'])
        else:
            item['year'] = -1

        if item['database'] == 'votos':
            item['uf'] = extract_uf(item['name'].split('_')[-1])

        if item['database'] in ['bem_candidato', 'filiados']:
            item['uf'] = extract_uf(item['name'].split('_')[-1])

        if item['database'] == 'filiados':
            item['party'] = extract_party('_'.join(item['name'].split('_')[1:-1]))

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

        if item['name'].startswith("detalhe"):
            item['uf'] = extract_uf(item['name'].split('_')[-1])
            item['table'] = "detalhe"

        elif item['name'].startswith('vot'):
            item['uf'] = extract_uf(item['name'].split('_')[-1])
            item['table'] = "votos"

        elif item['name'].startswith("cand"):
            item['table'] = "candidatos"

        elif item['name'].startswith("leg"):
            item['table'] = "legendas"

        return item
