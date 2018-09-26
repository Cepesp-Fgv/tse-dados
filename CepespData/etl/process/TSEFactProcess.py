import os
from _csv import QUOTE_ALL
from glob import glob

import pandas as pd

from etl.process.items import SourceFileItem
from web.cepesp.utils.data import resolve_conflicts


class TSEFactProcess:
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

    idx = [
        "ANO_ELEICAO",
        "CODIGO_CARGO",
        "NUMERO_CANDIDATO",
        "SIGLA_UE",
        "NUM_TURNO"
    ]

    idx_leg = [
        "ANO_ELEICAO",
        "CODIGO_CARGO",
        "NUMERO_PARTIDO",
        "SIGLA_UE",
        "NUM_TURNO"
    ]

    def __init__(self, mun_df_path, output):
        self.mun_df_path = mun_df_path
        self.output = output
        self.aux_mun = pd.read_csv(self.mun_df_path, sep=',', dtype=str)

    def handle(self, item: SourceFileItem):
        if item['database'] == "votos" and not self._done(item):
            cand = self.get_candidates(item['year'])
            leg = self.get_coalitions(item['year'])

            chunk = 1
            for vot in pd.read_csv(item['path'], sep=';', dtype=str, chunksize=10000):
                df = self.join_mun(vot)

                df['SIGLA_UE_2'] = df['SIGLA_UE']
                df.loc[df['CODIGO_CARGO'] == '1', 'SIGLA_UE'] = 'BR'

                df = self.join_candidatos(cand, df)
                df = self.join_legendas(df, leg)
                df = self.join_votos_legenda(df, leg)

                df['SIGLA_UE'] = df['SIGLA_UE_2']
                df.loc[df['NUMERO_CANDIDATO'] == '95', 'ID_LEGENDA'] = '1'
                df.loc[df['NUMERO_CANDIDATO'] == '96', 'ID_LEGENDA'] = '2'
                df = df[self.columns + ['ID_CANDIDATO', 'ID_LEGENDA']]

                self._save(df, item, chunk)

                chunk += 1

    def join_votos_legenda(self, df, leg):
        df = df.set_index(self.idx)
        df = df.merge(leg.rename(columns={'NUMERO_PARTIDO': 'NUMERO_CANDIDATO'}).set_index(self.idx),
                      how='left', left_index=True, right_index=True).reset_index()
        df.loc[df['ID_LEGENDA_x'].isnull(), 'ID_LEGENDA_x'] = df['ID_LEGENDA_y']
        df = resolve_conflicts(df)
        df.loc[df['ID_LEGENDA'].isnull(), 'ID_LEGENDA'] = '0'

        return df

    def join_legendas(self, df, leg):
        df = df.set_index(self.idx_leg)
        df = df.merge(leg.set_index(self.idx_leg), how='left', left_index=True, right_index=True).reset_index()
        df = resolve_conflicts(df)
        df.loc[df['ID_LEGENDA'].isnull(), 'ID_LEGENDA'] = '0'
        df = df[self.columns + ['SIGLA_UE_2', 'ID_CANDIDATO', 'ID_LEGENDA']]

        return df

    def join_candidatos(self, cand, df):
        df = df.set_index(self.idx)
        df = df.merge(cand.set_index(self.idx), how='left', left_index=True, right_index=True).reset_index()
        df = resolve_conflicts(df)
        df.loc[df['ID_CANDIDATO'].isnull(), 'ID_CANDIDATO'] = '0'
        df.loc[df['ID_CANDIDATO'] == '0', 'NUMERO_PARTIDO'] = '0'
        df.loc[df['NUMERO_CANDIDATO'] == '95', 'ID_CANDIDATO'] = '1'
        df.loc[df['NUMERO_CANDIDATO'] == '95', 'NUMERO_PARTIDO'] = '95'
        df.loc[df['NUMERO_CANDIDATO'] == '96', 'ID_CANDIDATO'] = '2'
        df.loc[df['NUMERO_CANDIDATO'] == '96', 'NUMERO_PARTIDO'] = '96'

        return df[self.columns + ['SIGLA_UE_2', 'NUMERO_PARTIDO', 'ID_CANDIDATO']]

    def join_mun(self, vot):
        df = vot.merge(self.aux_mun, on='COD_MUN_TSE', how='left', sort=False)
        df = resolve_conflicts(df, prefer='_y', drop='_x')
        df = df.rename(columns={'SIGLA_UF': 'UF'})

        return df

    def _save(self, df, item, chunk):
        output_path = os.path.join(self.output, "votos", "votsec", item['name'])

        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        header = chunk == 1
        mode = 'a' if chunk > 1 else 'w+'
        df.to_csv(output_path, mode=mode, header=header, compression='gzip', sep=';', encoding='utf-8', index=False,
                  quoting=QUOTE_ALL)

    def _done(self, item):
        output_path = os.path.join(self.output, "votos", "votsec", item['name'])
        return os.path.exists(output_path)

    def output_files(self):
        return glob(os.path.join(self.output, "votos", "votsec", '*.gz'))

    def get_coalitions(self, year):
        path = os.path.join(self.output, "dim_legendas", "legendas_%d.gz" % year)
        leg = pd.read_csv(path, sep=';', dtype=str)

        path_presidente = os.path.join(self.output, "dim_legendas", "legendas_%d_presidente.gz" % year)
        if os.path.exists(path_presidente):
            leg_pres = pd.read_csv(path_presidente, sep=';', dtype=str)
            leg = leg.append(leg_pres, ignore_index=True)

        return leg

    def get_candidates(self, year):
        path = os.path.join(self.output, "dim_candidatos", "candidato_%d.gz" % year)
        cand = pd.read_csv(path, sep=';', dtype=str)

        path_presidente = os.path.join(self.output, "dim_candidatos", "candidato_%d_presidente.gz" % year)
        if os.path.exists(path_presidente):
            cand_pres = pd.read_csv(path_presidente, sep=';', dtype=str)
            cand = cand.append(cand_pres, ignore_index=True)

        return cand
