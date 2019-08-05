import os
from _csv import QUOTE_ALL
from glob import glob

import pandas as pd

from web.cepesp.utils.data import resolve_conflicts


class VotesVotsecProcess:
    columns = [
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
        "QTDE_VOTOS"
    ]

    def __init__(self, mun_df_path, candidates_path, legendas_path, output):
        self.legendas_path = legendas_path
        self.candidates_path = candidates_path
        self.output = output
        self.aux_mun = pd.read_csv(mun_df_path, sep=',', dtype=str)

    def check(self, item):
        return item['database'] == "votos"

    def done(self, item):
        return os.path.exists(self._output(item))

    def handle(self, item):
        chunk = 0
        cand = self.get_candidates(item['year']).fillna("#NULO#")
        cand = cand.rename(columns={'SIGLA_UF': 'UF'})
        cand = cand[cand.COD_SITUACAO_CANDIDATURA != '3']  # Filtrar Inaptos

        leg = self.get_legendas(item['year']).fillna("#NULO#")
        leg = leg.rename(columns={'SIGLA_UF': 'UF'})

        for df in pd.read_csv(item['path'], sep=';', dtype=str, chunksize=100000):
            df['NUMERO_PARTIDO'] = df.NUMERO_CANDIDATO.str[0:2]
            df = self._process_joins(item, df, cand, leg)
            df = df[self.columns + ['ID_CANDIDATO', 'ID_LEGENDA']]
            self._save(df, item, chunk)

            chunk += 1

    def _process_joins(self, item, df, cand, leg):
        df = self.join_mun(df)

        size = len(df)
        df = self.join_candidatos(item, cand, df)
        self._validate_size('candidatos', size, df)

        df = self.join_legendas(item, df, leg)
        self._validate_size('legendas', size, df)

        if item['uf'] not in ['ZZ', 'BR', 'VT']:
            df = self.join_legendas_uf(df, leg)
            self._validate_size('legendas', size, df)

            df = self.join_legendas_no_job(df, leg)
            self._validate_size('legendas', size, df)

        return df

    def join_candidatos(self, item, cand, df):
        if item['uf'] == 'ZZ':
            idx = ["ANO_ELEICAO", "CODIGO_CARGO", "NUMERO_CANDIDATO", "NUM_TURNO"]
        else:
            idx = ["ANO_ELEICAO", "CODIGO_CARGO", "NUMERO_CANDIDATO", "NUM_TURNO", "SIGLA_UE"]

        cand = cand.drop_duplicates(idx)

        df = df.set_index(idx)
        df = df.merge(cand.set_index(idx), how='left', left_index=True, right_index=True).reset_index()
        df = resolve_conflicts(df)

        df.loc[df['ID_CANDIDATO'].isnull(), 'ID_CANDIDATO'] = '0'

        return df[self.columns + ['NUMERO_PARTIDO', 'ID_CANDIDATO']]

    def join_legendas(self, item, df, leg):
        if item['uf'] == 'ZZ':
            idx = ["ANO_ELEICAO", "CODIGO_CARGO", "NUMERO_PARTIDO"]
        else:
            idx = ["ANO_ELEICAO", "CODIGO_CARGO", "NUMERO_PARTIDO", "SIGLA_UE"]

        leg = leg.drop_duplicates(idx)

        df = df.set_index(idx)
        df = df.merge(leg.set_index(idx), how='left', left_index=True, right_index=True).reset_index()
        df = resolve_conflicts(df)

        df.loc[df['ID_LEGENDA'].isnull(), 'ID_LEGENDA'] = '0'

        return df[self.columns + ['NUMERO_PARTIDO', 'ID_CANDIDATO', 'ID_LEGENDA']]

    def join_legendas_uf(self, df, leg):
        idx = ["ANO_ELEICAO", "CODIGO_CARGO", "NUMERO_PARTIDO", "UF"]

        leg = leg.drop_duplicates(idx)

        df = df.set_index(idx)
        df = df.merge(leg.set_index(idx), how='left', left_index=True, right_index=True).reset_index()
        df.loc[df['ID_LEGENDA_x'] == '0', 'ID_LEGENDA_x'] = df['ID_LEGENDA_y']
        df = resolve_conflicts(df)

        df.loc[df['ID_LEGENDA'].isnull(), 'ID_LEGENDA'] = '0'

        return df[self.columns + ['NUMERO_PARTIDO', 'ID_CANDIDATO', 'ID_LEGENDA']]

    def join_legendas_no_job(self, df, leg):
        idx = ["ANO_ELEICAO", "NUMERO_PARTIDO", "UF"]

        leg = leg.drop_duplicates(idx)

        df = df.set_index(idx)
        df = df.merge(leg.set_index(idx), how='left', left_index=True, right_index=True).reset_index()
        df.loc[df['ID_LEGENDA_x'] == '0', 'ID_LEGENDA_x'] = df['ID_LEGENDA_y']
        df = resolve_conflicts(df)

        df.loc[df['ID_LEGENDA'].isnull(), 'ID_LEGENDA'] = '0'

        return df[self.columns + ['NUMERO_PARTIDO', 'ID_CANDIDATO', 'ID_LEGENDA']]

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

    def get_legendas(self, year):
        df = None

        path = os.path.join(self.legendas_path, "legendas_%d.gz" % year)
        if os.path.exists(path):
            df = pd.read_csv(path, sep=';', dtype=str)

        path = os.path.join(self.legendas_path, "legendas_%d_presidente.gz" % year)
        if os.path.exists(path):
            pres_df = pd.read_csv(path, sep=';', dtype=str)
            df = df.append(pres_df, ignore_index=True) if df is not None else pres_df

        return df

    def get_candidates(self, year):
        df = None

        path = os.path.join(self.candidates_path, "candidato_%d.gz" % year)
        if os.path.exists(path):
            df = pd.read_csv(path, sep=';', dtype=str)

        path = os.path.join(self.candidates_path, "candidato_%d_presidente.gz" % year)
        if os.path.exists(path):
            pres_df = pd.read_csv(path, sep=';', dtype=str)
            df = df.append(pres_df, ignore_index=True) if df is not None else pres_df

        return df

    def output_files(self):
        return glob(os.path.join(self.output, '*.gz'))

    def _validate_size(self, join, before, df):
        after = len(df)
        if after > before:
            raise Exception(f'{after - before} duplicated values on {join}')
