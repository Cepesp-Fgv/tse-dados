import os
from glob import glob

from scrapy.crawler import CrawlerProcess

from etl.crawler.spiders import TSESpider


class CrawlTSEDataProcess:

    def __init__(self, jobs, years, download_output, processed_output):
        self.output = processed_output
        self.process = CrawlerProcess({
            'LOG_LEVEL': 'WARNING',
            'USER_AGENT': 'CEPESP-FGV Crawler (+http://cepesp.io)',
            'FILES_STORE': download_output,
            'PROCESSED_STORE': processed_output,
            'DOWNLOAD_TIMEOUT': 36000,

            'JOBS': jobs,
            'YEARS': years,
            'DATABASES': [
                "odsele/votacao_secao",
                "eleicoes/eleicoes2012/votosecao",
                "bem_candidato",
                "odsele/detalhe_votacao_secao",
                "eleitorado/filiados"
            ],

            'ITEM_PIPELINES': {
                'crawler.pipelines.TSEFilesPipeline': 100,
                'crawler.pipelines.ProcessItemPipeline': 200
            }

        })
        self.process.crawl(TSESpider)

    def start(self):
        self.process.start()

    def output_files(self):
        return glob(os.path.join(self.output, '*.gz'))
