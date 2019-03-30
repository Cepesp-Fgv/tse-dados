# -*- coding: utf-8 -*-
import os
import re
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

    rename_2018 = {
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
    }

    bem_candidato = [
        "DATA_GERACAO",
        "HORA_GERACAO",
        "ANO_ELEICAO",
        "DESCRICAO_ELEICAO",
        "SIGLA_UF",
        "SQ_CANDIDATO",
        "CD_TIPO_BEM_CANDIDATO",
        "DS_TIPO_BEM_CANDIDATO",
        "DETALHE_BEM",
        "VALOR_BEM",
        "DATA_ULTIMA_ATUALIZACAO",
        "HORA_ULTIMA_ATUALIZACAO",
    ]

    bem_candidato_rename_2018 = {
        "DT_GERACAO": "DATA_GERACAO",
        "HH_GERACAO": "HORA_GERACAO",
        "DS_ELEICAO": "DESCRICAO_ELEICAO",
        "SG_UF": "SIGLA_UF",
        "SG_UE": "SIGLA_UE",
        "NM_UE": "NOME_UE",
        "VR_BEM_CANDIDATO": "VALOR_BEM",
        "DS_BEM_CANDIDATO": "DETALHE_BEM",
        "DT_ULTIMA_ATUALIZACAO": "DATA_ULTIMA_ATUALIZACAO",
        "HH_ULTIMA_ATUALIZACAO": "HORA_ULTIMA_ATUALIZACAO"
    }

    detalhe = [
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
        "QTD_APTOS",
        "QTD_COMPARECIMENTO",
        "QTD_ABSTENCOES",
        "QT_VOTOS_NOMINAIS",
        "QT_VOTOS_BRANCOS",
        "QT_VOTOS_NULOS",
        "QT_VOTOS_LEGENDA",
        "QT_VOTOS_ANULADOS_APU_SEP",
    ]

    detalhe_2018 = {
        "DT_GERACAO": "DATA_GERACAO",
        "HH_GERACAO": "HORA_GERACAO",
        "DT_ELEICAO": "DATA_ELEICAO",
        "DS_ELEICAO": "DESCRICAO_ELEICAO",
        "NR_TURNO": "NUM_TURNO",
        "SG_UF": "SIGLA_UF",
        "SG_UE": "SIGLA_UE",
        "NM_UE": "DESCRICAO_UE",
        "CD_MUNICIPIO": "COD_MUN_TSE",
        "NM_MUNICIPIO": "NOME_MUNICIPIO",
        "NR_ZONA": "NUM_ZONA",
        "NR_SECAO": "NUM_SECAO",
        "CD_CARGO": "CODIGO_CARGO",
        "DS_CARGO": "DESCRICAO_CARGO",
        "QT_APTOS": "QTD_APTOS",
        "QT_COMPARECIMENTO": "QTD_COMPARECIMENTO",
        "QT_ABSTENCOES": "QTD_ABSTENCOES",
        "QT_VOTOS_PENDENTES": "QT_VOTOS_ANULADOS_APU_SEP",
    }

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
        if len(item['files']) == 0:
            raise DropItem("No file downloaded")

        file_path = os.path.join(self.source, item['files'][0]['path'])

        if 'bem_candidato' in item['name']:

            if item['year'] in [2014, 2016, 2018]:
                self._extract_files(file_path, rename=self.bem_candidato_rename_2018)
            else:
                self._extract_files(file_path, columns=self.bem_candidato)

        elif 'detalhe' in item['name']:

            if item['year'] == 2018:
                self._extract_files(file_path, rename=self.detalhe_2018)
            else:
                self._extract_files(file_path, columns=self.detalhe)

        elif 'votos' in item['name']:

            if item['year'] == 2018:
                self._extract_files(file_path, rename=self.rename_2018)
            else:
                self._extract_files(file_path, columns=self.columns)

        else:
            self._extract_files(file_path)

        return item

    def _extract_files(self, file_path, sep=';', columns=None, rename=None):
        with zipfile.ZipFile(file_path) as z:
            for file in z.namelist():
                file_new = re.sub(r'(\.txt|\.csv)', '.gz', file)
                output_path = os.path.join(self.output, file_new)

                if not os.path.exists(output_path) and (file.endswith('.txt') or file.endswith('.csv')):

                    directory = os.path.dirname(output_path)
                    if not os.path.isdir(directory):
                        os.makedirs(directory)

                    with z.open(file) as f:

                        if columns is None or len(columns) == 0:
                            df = pd.read_csv(f, sep=sep, dtype=str, encoding='latin1', header=0)
                        else:
                            df = pd.read_csv(f, sep=sep, dtype=str, encoding='latin1', names=columns)

                        if rename is not None:
                            df.rename(columns=rename, inplace=True)

                        df.to_csv(output_path, compression='gzip', sep=';', encoding='utf-8', index=False,
                                  quoting=QUOTE_ALL)
