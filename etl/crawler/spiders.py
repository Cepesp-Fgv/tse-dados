# -*- coding: utf-8 -*-
import scrapy
from etl.crawler.items import TSEFileItem


class TSESpider(scrapy.Spider):
    name = "tse"
    start_urls = ['http://www.tse.jus.br/hotsites/pesquisas-eleitorais/']
    allowed_domains = ['agencia.tse.jus.br', 'www.tse.jus.br']
    loaded_parties = False
    parties = ["avante", "dc", "dem", "mdb", "novo", "patri", "pc_do_b", "pcb", "pco", "pdt", "phs", "pmb", "pmn",
               "pode", "pp", "ppl", "pps", "pr", "prb", "pros", "prp", "prtb", "psb", "psc", "psd", "psdb", "psl",
               "psol", "pstu", "pt", "ptb", "ptc", "pv", "rede", "solidariedade"]
    ufs = ["ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg", "ms", "mt", "pa", "pb", "pe", "pi", "pr",
           "rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to"]

    def parse(self, response):
        if not self.loaded_parties:
            for party in self.parties:
                for uf in self.ufs:
                    url = f"http://agencia.tse.jus.br/estatistica/sead/eleitorado/filiados/uf/filiados_{party}_{uf}.zip"
                    item = TSEFileItem.create(url)
                    if self.is_valid(item):
                        yield item

            self.loaded_parties = True

        for link in response.css('a::attr(href)'):
            href = link.extract()
            if href.find('.zip') != -1 and href.find('.sha1') == -1:
                item = TSEFileItem.create(href)
                if self.is_valid(item):
                    yield item
            elif href.find('.html') != -1:
                yield response.follow(link, self.parse)

    def is_valid(self, item):
        found_db = False
        for db in self.settings.get('DATABASES'):
            if db in item['path']:
                found_db = True

        if not found_db:
            return False

        if item['year'] and item['year'] not in self.settings.get('YEARS'):
            return False

        if item['year'] in [1998, 2006, 2010] and 'BR' in item['name']:
            return False

        return True
