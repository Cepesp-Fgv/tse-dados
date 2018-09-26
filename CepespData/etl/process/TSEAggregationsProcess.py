import os
from _csv import QUOTE_ALL
from glob import glob

import pandas as pd


class TSEAggregationsProcess:

    columns_by_regional = {

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

    reg = {
        2: 'uf',
        4: 'meso',
        5: 'micro',
        6: 'municipio',
        7: 'munzona',
        8: 'zona',
    }

    def __init__(self, output):
        self.output = output

    def handle(self, item):
        if item['database'] == 'votos' and not self._done(item):

            df = pd.read_csv(item['path'], sep=';', dtype=str)
            df['QTDE_VOTOS'] = pd.to_numeric(df['QTDE_VOTOS'], errors='coerce')

            for (regional_id, columns) in self.columns_by_regional.items():
                group = list(set(columns) - {'QTDE_VOTOS'})
                group_df = df.groupby(group, as_index=False).sum()
                self._save(group_df[columns], item, regional_id)

    def _save(self, df, item, regional_id):
        regional_name = self.reg[regional_id]
        output_path = os.path.join(self.output, "votos", regional_name, item['name'])

        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        df.to_csv(output_path, header=True, compression='gzip', sep=';', encoding='utf-8', index=False, quoting=QUOTE_ALL)

    def output_files(self):
        files = glob(os.path.join(self.output, 'dim_candidatos', '*.gz'))
        files += glob(os.path.join(self.output, 'dim_legendas', '*.gz'))

        for regional_id in self.columns_by_regional.keys():
            regional_name = self.reg[regional_id]
            files += glob(os.path.join(self.output, "votos", regional_name, '*.gz'))

        files += glob(os.path.join(self.output, "votos", "votsec", '*.gz'))

        return files

    def _done(self, item):
        for regional_id in self.columns_by_regional.keys():
            regional_name = self.reg[regional_id]
            output_path = os.path.join(self.output, "votos", regional_name, item['name'])
            if not os.path.exists(output_path):
                return False

        return True
