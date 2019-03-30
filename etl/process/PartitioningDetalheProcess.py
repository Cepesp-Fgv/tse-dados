import os
import pandas as pd
from _csv import QUOTE_ALL


class PartitioningDetalheProcess:
    columns = {

        # VOTACAO SECAO
        9: [
            'ANO_ELEICAO',
            'NUM_TURNO',
            'NUM_ZONA',
            'NUM_SECAO',
            'COD_MUN_TSE',
            'COD_MUN_IBGE',
            'NOME_MUNICIPIO',
            'CODIGO_MICRO',
            'NOME_MICRO',
            'CODIGO_MESO',
            'NOME_MESO',
            'UF',
            'NOME_UF',
            'CODIGO_MACRO',
            'NOME_MACRO',
            'DESCRICAO_ELEICAO',
            'CODIGO_CARGO',
            'DESCRICAO_CARGO',
            'QTD_APTOS',
            'QTD_COMPARECIMENTO',
            'QTD_ABSTENCOES',
            'QT_VOTOS_NOMINAIS',
            'QT_VOTOS_BRANCOS',
            'QT_VOTOS_NULOS',
            'QT_VOTOS_LEGENDA',
            'QT_VOTOS_ANULADOS_APU_SEP',
        ],

        # ZONA
        8: [
            'ANO_ELEICAO',
            'NUM_TURNO',
            'NUM_ZONA',
            'CODIGO_MICRO',
            'NOME_MICRO',
            'CODIGO_MESO',
            'NOME_MESO',
            'UF',
            'NOME_UF',
            'CODIGO_MACRO',
            'NOME_MACRO',
            'DESCRICAO_ELEICAO',
            'CODIGO_CARGO',
            'DESCRICAO_CARGO',
            'QTD_APTOS',
            'QTD_COMPARECIMENTO',
            'QTD_ABSTENCOES',
            'QT_VOTOS_NOMINAIS',
            'QT_VOTOS_BRANCOS',
            'QT_VOTOS_NULOS',
            'QT_VOTOS_LEGENDA',
            'QT_VOTOS_ANULADOS_APU_SEP',
        ],

        # MUNZONA
        7: [
            'ANO_ELEICAO',
            'NUM_TURNO',
            'NUM_ZONA',
            'COD_MUN_TSE',
            'COD_MUN_IBGE',
            'NOME_MUNICIPIO',
            'CODIGO_MICRO',
            'NOME_MICRO',
            'CODIGO_MESO',
            'NOME_MESO',
            'UF',
            'NOME_UF',
            'CODIGO_MACRO',
            'NOME_MACRO',
            'DESCRICAO_ELEICAO',
            'CODIGO_CARGO',
            'DESCRICAO_CARGO',
            'QTD_APTOS',
            'QTD_COMPARECIMENTO',
            'QTD_ABSTENCOES',
            'QT_VOTOS_NOMINAIS',
            'QT_VOTOS_BRANCOS',
            'QT_VOTOS_NULOS',
            'QT_VOTOS_LEGENDA',
            'QT_VOTOS_ANULADOS_APU_SEP',
        ],

        # MUNICIPIO
        6: [
            'ANO_ELEICAO',
            'NUM_TURNO',
            'COD_MUN_TSE',
            'COD_MUN_IBGE',
            'NOME_MUNICIPIO',
            'CODIGO_MICRO',
            'NOME_MICRO',
            'CODIGO_MESO',
            'NOME_MESO',
            'UF',
            'NOME_UF',
            'CODIGO_MACRO',
            'NOME_MACRO',
            'DESCRICAO_ELEICAO',
            'CODIGO_CARGO',
            'DESCRICAO_CARGO',
            'QTD_APTOS',
            'QTD_COMPARECIMENTO',
            'QTD_ABSTENCOES',
            'QT_VOTOS_NOMINAIS',
            'QT_VOTOS_BRANCOS',
            'QT_VOTOS_NULOS',
            'QT_VOTOS_LEGENDA',
            'QT_VOTOS_ANULADOS_APU_SEP',
        ],

        # MICRO
        5: [
            'ANO_ELEICAO',
            'NUM_TURNO',
            'CODIGO_MICRO',
            'NOME_MICRO',
            'CODIGO_MESO',
            'NOME_MESO',
            'UF',
            'NOME_UF',
            'CODIGO_MACRO',
            'NOME_MACRO',
            'DESCRICAO_ELEICAO',
            'CODIGO_CARGO',
            'DESCRICAO_CARGO',
            'QTD_APTOS',
            'QTD_COMPARECIMENTO',
            'QTD_ABSTENCOES',
            'QT_VOTOS_NOMINAIS',
            'QT_VOTOS_BRANCOS',
            'QT_VOTOS_NULOS',
            'QT_VOTOS_LEGENDA',
            'QT_VOTOS_ANULADOS_APU_SEP',
        ],

        # MESO
        4: [
            'ANO_ELEICAO',
            'NUM_TURNO',
            'CODIGO_MESO',
            'NOME_MESO',
            'UF',
            'NOME_UF',
            'CODIGO_MACRO',
            'NOME_MACRO',
            'DESCRICAO_ELEICAO',
            'CODIGO_CARGO',
            'DESCRICAO_CARGO',
            'QTD_APTOS',
            'QTD_COMPARECIMENTO',
            'QTD_ABSTENCOES',
            'QT_VOTOS_NOMINAIS',
            'QT_VOTOS_BRANCOS',
            'QT_VOTOS_NULOS',
            'QT_VOTOS_LEGENDA',
            'QT_VOTOS_ANULADOS_APU_SEP',
        ],

        # UF
        2: [
            'ANO_ELEICAO',
            'NUM_TURNO',
            'UF',
            'NOME_UF',
            'CODIGO_MACRO',
            'NOME_MACRO',
            'DESCRICAO_ELEICAO',
            'CODIGO_CARGO',
            'DESCRICAO_CARGO',
            'QTD_APTOS',
            'QTD_COMPARECIMENTO',
            'QTD_ABSTENCOES',
            'QT_VOTOS_NOMINAIS',
            'QT_VOTOS_BRANCOS',
            'QT_VOTOS_NULOS',
            'QT_VOTOS_LEGENDA',
            'QT_VOTOS_ANULADOS_APU_SEP',
        ],

    }

    def __init__(self, jobs, output):
        self.output = output
        self.jobs = jobs
        self.aggregations = {2: 'uf', 4: 'meso', 5: 'micro', 6: 'mun', 7: 'munzona', 8: 'zona', 9: 'votsec'}
        self.sum_cols = {'QTD_APTOS', 'QTD_COMPARECIMENTO', 'QTD_ABSTENCOES', 'QT_VOTOS_NOMINAIS', 'QT_VOTOS_BRANCOS',
                         'QT_VOTOS_NULOS', 'QT_VOTOS_LEGENDA', 'QT_VOTOS_ANULADOS_APU_SEP'}

    def check(self, item):
        return item['table'] == 'detalhe'

    def done(self, item):
        for code in self.aggregations.keys():
            for job in self._get_jobs(item):
                if not os.path.exists(self._output(item, code, job)):
                    return False

        return True

    def handle(self, item):
        df = pd.read_csv(item['path'], sep=';', dtype=str)
        for c in self.sum_cols:
            df[c] = pd.to_numeric(df[c], errors='coerce')
        df.fillna('#NE#')

        for (aggregation, columns) in self.columns.items():
            if aggregation < 9:
                group = list(set(columns) - self.sum_cols)
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
        return os.path.join(self.output, aggregation_name, str(item['year']), str(job), item['name'])

    def _get_jobs(self, item):
        if item['uf'] == 'ZZ' or (item['year'] in [2018, 2014, 2002] and item['uf'] == 'BR'):
            return [1]
        elif item['year'] in [1998, 2002, 2006, 2010, 2014, 2018]:
            return [1, 3, 5, 6, 7]
        else:
            return [11, 13]
