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

    def __init__(self, source, output, years):
        self.source = source
        self.output = output
        self.years = years

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            source=crawler.settings.get('FILES_STORE'),
            output=crawler.settings.get('PROCESSED_STORE'),
            years=crawler.settings.get('YEARS'),
        )

    def process_item(self, item, spider):
        if item['year'] == 2012:
            uf = item['uf']
            turn = item['turn']
            name = f'votacao_secao_2012_{uf}_{turn}.gz'
        else:
            name = item['name'].replace('.zip', '.gz')

        output_path = os.path.join(self.output, name)

        if not os.path.exists(output_path) and item['year'] in self.years:
            if len(item['files']) == 0:
                raise DropItem("No file downloaded")

            file_path = os.path.join(self.source, item['files'][0]['path'])

            directory = os.path.dirname(output_path)
            if not os.path.isdir(directory):
                os.makedirs(directory)

            with zipfile.ZipFile(file_path) as z:
                for file in z.namelist():
                    if '.txt' in file or '.csv' in file:
                        self.extract_data(z, file, output_path, item['year'] == 2018)

        return item

    def extract_data(self, z, file_name, output_path, header=False):
        with z.open(file_name) as f:
            if header:
                df = pd.read_csv(f, sep=';', dtype=str, encoding='latin1', header=0)
                df.rename(columns={
                    "DT_GERACAO": "DATA_GERACAO",
                    "HH_GERACAO": "HORA_GERACAO",
                    "DS_ELEICAO": "DESCRICAO_ELEICAO",
                    "NR_TURNO": "NUM_TURNO",
                    "SG_UF": "SIGLA_UF",
                    "SG_UE": "SIGLA_UE",
                    "NM_UE": "NOME_UE",
                    "CD_MUNICIPIO": "COD_MUN_TSE",
                    "NM_MUNICIPIO": "NOME_MUNICIPIO",
                    "NR_ZONA": "NUM_ZONA",
                    "NR_SECAO": "NUM_SECAO",
                    "CD_CARGO": "CODIGO_CARGO",
                    "DS_CARGO": "DESCRICAO_CARGO",
                    "NR_VOTAVEL": "NUMERO_CANDIDATO",
                    "QT_VOTOS": "QTDE_VOTOS",
                    "NM_VOTAVEL": "NOME_CANDIDATO"
                }, inplace=True)
            else:
                df = pd.read_csv(f, sep=';', dtype=str, encoding='latin1', names=self.columns)

            df.to_csv(output_path, compression='gzip', sep=';', encoding='utf-8', index=False, quoting=QUOTE_ALL)
