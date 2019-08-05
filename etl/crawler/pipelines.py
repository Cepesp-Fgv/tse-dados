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
        "SEQUENCIAL_CANDIDATO",
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
        "HH_ULTIMA_ATUALIZACAO": "HORA_ULTIMA_ATUALIZACAO",
        "SQ_CANDIDATO": "SEQUENCIAL_CANDIDATO"
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

    rename_filiados = {
        "DATA DA EXTRACAO": "DATA_EXTRACAO",
        "HORA DA EXTRACAO": "HORA_EXTRACAO",
        "NUMERO DA INSCRICAO": "NUMERO_INSCRICAO",
        "NOME DO FILIADO": "NOME_FILIADO",
        "SIGLA DO PARTIDO": "SIGLA_PARTIDO",
        "NOME DO PARTIDO": "NOME_PARTIDO",
        "UF": "UF",
        "CODIGO DO MUNICIPIO": "COD_MUN_TSE",
        "NOME DO MUNICIPIO": "NOME_MUNICIPIO",
        "ZONA ELEITORAL": "NUM_ZONA",
        "SECAO ELEITORAL": "NUM_SECAO",
        "DATA DA FILIACAO": "DATA_FILIACAO",
        "SITUACAO DO REGISTRO": "SITUACAO_REGISTRO",
        "TIPO DO REGISTRO": "TIPO_REGISTRO",
        "DATA DO PROCESSAMENTO": "DATA_PROCESSAMENTO",
        "DATA DA DESFILIACAO": "DATA_DESFILIACAO",
        "DATA DO CANCELAMENTO": "DATA_CANCELAMENTO",
        "DATA DA REGULARIZACAO": "DATA_REGULARIZACAO",
        "MOTIVO DO CANCELAMENTO": "MOTIVO_CANCELAMENTO"
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

        elif 'votacao' in item['name']:

            if item['year'] == 2018:
                self._extract_files(file_path, rename=self.rename_2018)
            else:
                self._extract_files(file_path, columns=self.columns)

        elif 'filiados' in item['name']:

            self._extract_files(file_path, rename=self.rename_filiados, filter_contains='filiados_')

        else:
            self._extract_files(file_path)

        return item

    def _extract_files(self, file_path, sep=';', columns=None, rename=None, filter_contains=None):
        with zipfile.ZipFile(file_path) as z:
            for file in z.namelist():
                if (filter_contains is None or filter_contains in file) \
                        and (file.endswith('.txt') or file.endswith('.csv')):

                    file_new = re.sub(r'(\.txt|\.csv)', '.gz', file)
                    file_new = file_new.split('/')[-1]  # skip inner directories
                    output_path = os.path.join(self.output, file_new)

                    if not os.path.exists(output_path):

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
