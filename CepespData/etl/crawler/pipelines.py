# -*- coding: utf-8 -*-
import os
import zipfile
from _csv import QUOTE_ALL

import pandas as pd
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

from etl.crawler.items import TSEFileItem


class TSEFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        item = TSEFileItem.create(request.url)
        return item['name']


class ProcessItemPipeline:
    columns = [
        "DATA_GERACAO",
        "HORA_GERACAO",
        "ANO_ELEICAO",
        "NUM_TURNO",
        "DESCRICAO_ELEICAO",
        "SIGLA_UF",
        "SIGLA_UE",
        "COD_MUN_TSE",
        "NOME_MUNICIPIO",
        "NUM_ZONA",
        "NUM_SECAO",
        "CODIGO_CARGO",
        "DESCRICAO_CARGO",
        "NUMERO_CANDIDATO",
        "QTDE_VOTOS"
    ]

    def __init__(self, source, output):
        self.source = source
        self.output = output

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            source=crawler.settings.get('FILES_STORE'),
            output=crawler.settings.get('PROCESSED_STORE'),
        )

    def process_item(self, item, spider):
        file_name = item['name'].replace('.zip', '.txt')
        output_path = os.path.join(self.output, item['name'].replace('.zip', '.gz'))

        if not os.path.exists(output_path):
            if len(item['files']) == 0:
                raise DropItem("No file downloaded")

            file_path = os.path.join(self.source, item['files'][0]['path'])

            directory = os.path.dirname(output_path)
            if not os.path.isdir(directory):
                os.makedirs(directory)

            with zipfile.ZipFile(file_path) as z:
                try:
                    with z.open(file_name) as f:
                        df = pd.read_csv(f, sep=';', dtype=str, encoding='latin1', names=self.columns)
                        df.to_csv(output_path, compression='gzip', sep=';', encoding='utf-8', index=False,
                                  quoting=QUOTE_ALL)
                except KeyError as e:
                    raise DropItem(str(e))

        return item
