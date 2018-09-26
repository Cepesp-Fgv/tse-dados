import os
from _csv import QUOTE_ALL

import pandas as pd

from etl.process.items import SourceFileItem


class OrganizingProcess:
    # region columns = {...}
    columns = {
        "mun": [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "COD_MUN_TSE",
            "COD_MUN_IBGE",
            "NOME_MUNICIPIO",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "SIGLA_UE",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
        ],

        "munzona": [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "COD_MUN_TSE",
            "COD_MUN_IBGE",
            "NOME_MUNICIPIO",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "SIGLA_UE",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
        ],

        "micro": [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "SIGLA_UE",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
        ]
    }

    # endregion

    def __init__(self, jobs, mun_df_path, output):
        self.jobs = jobs
        self.output = output
        self.mun_df = pd.read_csv(mun_df_path, sep=',', dtype=str)

    def handle(self, item: SourceFileItem):
        df = pd.read_csv(item['path'], sep=';', dtype=str)
        df.CODIGO_CARGO = pd.to_numeric(df.CODIGO_CARGO, errors='coerce')

        if item['database'] == 'votos':
            self._handle_votos(df, item)

        if item['database'] in ['candidatos', 'legendas']:
            self._handle_candidatos_legendas(df, item)

    def _handle_candidatos_legendas(self, df, item):
        for job in self.jobs:
            job_df = df[df.CODIGO_CARGO == job]

            if len(job_df) > 0:
                output_path = os.path.join(self.output, item['database'], str(item['year']), str(job), item['name'])
                self._save(job_df, output_path)

    def _save(self, job_df, output_path):
        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        if os.path.exists(output_path):
            return

        job_df.to_csv(output_path, compression='gzip', sep=';', encoding='utf-8', index=False, quoting=QUOTE_ALL)

    def _handle_votos(self, df, item):
        df.QTDE_VOTOS = pd.to_numeric(df.QTDE_VOTOS, errors='coerce')

        df = df.merge(self.mun_df, on='COD_MUN_TSE', how='left', sort=False)
        df = df.rename(columns={'SIGLA_UF_y': 'UF', 'NOME_MUNICIPIO_y': 'NOME_MUNICIPIO'})

        self._save_votos(df, "votsec", item)

        for (group, columns) in self.columns.items():
            print(group, item['year'])
            df = df.groupby(columns, as_index=False).sum()
            self._save_votos(df, group, item)

    def _save_votos(self, df, regional, item):
        for job in self.jobs:
            job_df = df[df.CODIGO_CARGO == job]

            if len(job_df) > 0:
                output_path = os.path.join(self.output, 'votos', regional, str(item['year']), str(job), item['name'])
                self._save(job_df, output_path)