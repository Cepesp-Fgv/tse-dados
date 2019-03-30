import os
from _csv import QUOTE_ALL
from glob import glob

import pandas as pd

from web.cepesp.utils.data import resolve_conflicts


class DetalheVotSecProcess:
    columns = [
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
    ]

    def __init__(self, mun_df_path, output):
        self.output = output
        self.aux_mun = pd.read_csv(mun_df_path, sep=',', dtype=str)

    def check(self, item):
        return item['database'] == "detalhe"

    def done(self, item):
        return os.path.exists(self._output(item))

    def handle(self, item):
        chunk = 0

        for df in pd.read_csv(item['path'], sep=';', dtype=str, chunksize=100000):
            df = self.join_mun(df)
            df = df[self.columns]
            self._save(df, item, chunk)

            chunk += 1

    def join_mun(self, vot):
        df = vot.merge(self.aux_mun, on='COD_MUN_TSE', how='left', sort=False)
        df = resolve_conflicts(df, prefer='_y', drop='_x')
        df = df.rename(columns={'SIGLA_UF': 'UF'})

        return df

    def _output(self, item):
        return os.path.join(self.output, item['name'])

    def _save(self, df, item, chunk):
        output_path = self._output(item)

        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        header = chunk == 0
        mode = 'a' if chunk > 0 else 'w+'
        df.to_csv(output_path, mode=mode, header=header, compression='gzip', sep=';', encoding='utf-8', index=False,
                  quoting=QUOTE_ALL)

    def output_files(self):
        return glob(os.path.join(self.output, '*.gz'))
