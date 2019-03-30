import os
import pandas as pd
from _csv import QUOTE_ALL


class PartitioningVotesProcess:

    columns = {

        # VOTACAO SECAO
        9: [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "NUM_SECAO",
            "NUM_ZONA",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "COD_MUN_TSE",
            "COD_MUN_IBGE",
            "NOME_MUNICIPIO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "SIGLA_UE",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS",
            "ID_CANDIDATO",
            "ID_LEGENDA"
        ],

        # ZONA
        8: [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "NUM_ZONA",
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
            "QTDE_VOTOS",
            "ID_CANDIDATO",
            "ID_LEGENDA"
        ],

        # MUNZONA
        7: [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "NUM_ZONA",
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
            "QTDE_VOTOS",
            "ID_CANDIDATO",
            "ID_LEGENDA"
        ],

        # MUNICIPIO
        6: [
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
            "QTDE_VOTOS",
            "ID_CANDIDATO",
            "ID_LEGENDA"
        ],

        # MICRO
        5: [
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
            "QTDE_VOTOS",
            "ID_CANDIDATO",
            "ID_LEGENDA"
        ],

        # MESO
        4: [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
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
            "QTDE_VOTOS",
            "ID_CANDIDATO",
            "ID_LEGENDA"
        ],

        # UF
        2: [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
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
            "QTDE_VOTOS",
            "ID_CANDIDATO",
            "ID_LEGENDA"
        ],

    }

    def __init__(self, jobs, output):
        self.output = output
        self.jobs = jobs
        self.aggregations = {2: 'uf', 4: 'meso', 5: 'micro', 6: 'mun', 7: 'munzona', 8: 'zona', 9: 'votsec'}

    def check(self, item):
        return item['table'] == 'votos'

    def done(self, item):
        for code in self.aggregations.keys():
            for job in self._get_jobs(item):
                if not os.path.exists(self._output(item, code, job)):
                    return False

        return True

    def handle(self, item):
        df = pd.read_csv(item['path'], sep=';', dtype=str)
        df['QTDE_VOTOS'] = pd.to_numeric(df['QTDE_VOTOS'], errors='coerce')
        df.fillnan('#NE#')

        for (aggregation, columns) in self.columns.items():
            if aggregation < 9:
                group = list(set(columns) - {'QTDE_VOTOS'})
                group_df = df.groupby(group, as_index=False).sum()
                group_df = group_df[columns]
            else:
                group_df = df[columns]

            for job in self.jobs:
                if not os.path.exists(self._output(item, aggregation, job)):
                    job_df = group_df[group_df['CODIGO_CARGO'] == str(job)]
                    if not job_df.empty:
                        self._save(job_df, item, aggregation, job)

    def _save(self, df, item, aggregation, job):
        output_path = self._output(item, aggregation, job)

        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        df.to_csv(output_path, header=True, compression='gzip', sep=';', encoding='utf-8', index=False,
                  quoting=QUOTE_ALL)

    def _output(self, item, aggregation, job):
        aggregation_name = self.aggregations[aggregation]
        return os.path.join(self.output, aggregation_name, str(item['year']), str(job), item['uf'], item['name'])

    def _get_jobs(self, item):
        if item['uf'] == 'ZZ' or (item['year'] in [2018, 2014, 2002] and item['uf'] == 'BR'):
            return [1]
        elif item['year'] in [1998, 2002, 2006, 2010, 2014, 2018]:
            return [1, 3, 5, 6, 7]
        else:
            return [11, 13]

