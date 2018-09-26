import os
from _csv import QUOTE_ALL

import pandas as pd

from etl.process.items import SourceFileItem


class TSEDimensionsProcessor:
    candidatos = [
        "ID_CANDIDATO",
        "DATA_GERACAO",
        "HORA_GERACAO",
        "ANO_ELEICAO",
        "NUM_TURNO",
        "DESCRICAO_ELEICAO",
        "SIGLA_UF",
        "SIGLA_UE",
        "DESCRICAO_UE",
        "CODIGO_CARGO",
        "DESCRICAO_CARGO",
        "NOME_CANDIDATO",
        "SEQUENCIAL_CANDIDATO",
        "NUMERO_CANDIDATO",
        "CPF_CANDIDATO",
        "NOME_URNA_CANDIDATO",
        "COD_SITUACAO_CANDIDATURA",
        "DES_SITUACAO_CANDIDATURA",
        "NUMERO_PARTIDO",
        "SIGLA_PARTIDO",
        "NOME_PARTIDO",
        "CODIGO_LEGENDA",
        "SIGLA_LEGENDA",
        "COMPOSICAO_LEGENDA",
        "NOME_COLIGACAO",
        "CODIGO_OCUPACAO",
        "DESCRICAO_OCUPACAO",
        "DATA_NASCIMENTO",
        "NUM_TITULO_ELEITORAL_CANDIDATO",
        "IDADE_DATA_ELEICAO",
        "CODIGO_SEXO",
        "DESCRICAO_SEXO",
        "COD_GRAU_INSTRUCAO",
        "DESCRICAO_GRAU_INSTRUCAO",
        "CODIGO_ESTADO_CIVIL",
        "DESCRICAO_ESTADO_CIVIL",
        "CODIGO_COR_RACA",
        "DESCRICAO_COR_RACA",
        "CODIGO_NACIONALIDADE",
        "DESCRICAO_NACIONALIDADE",
        "SIGLA_UF_NASCIMENTO",
        "CODIGO_MUNICIPIO_NASCIMENTO",
        "NOME_MUNICIPIO_NASCIMENTO",
        "DESPESA_MAX_CAMPANHA",
        "COD_SIT_TOT_TURNO",
        "DESC_SIT_TOT_TURNO",
        "EMAIL_CANDIDATO"
    ]

    legendas = [
        "ID_LEGENDA",
        "ANO_ELEICAO",
        "CODIGO_CARGO",
        "COMPOSICAO_COLIGACAO",
        "DATA_GERACAO",
        "DESCRICAO_CARGO",
        "DESCRICAO_ELEICAO",
        "DESCRICAO_UE",
        "HORA_GERACAO",
        "NOME_COLIGACAO",
        "NOME_PARTIDO",
        "NUMERO_PARTIDO",
        "NUM_TURNO",
        "SEQUENCIA_COLIGACAO",
        "SIGLA_COLIGACAO",
        "SIGLA_PARTIDO",
        "SIGLA_UE",
        "SIGLA_UF",
        "TIPO_LEGENDA"
    ]

    def __init__(self, mun_df_path, output):
        self.output = output
        self.last_cand_id = 1
        self.last_leg_id = 1
        self.aux_mun = pd.read_csv(mun_df_path, sep=',', dtype=str)

    def handle(self, item: SourceFileItem):
        if item['database'] in ["candidatos", "legendas"] and not self._done(item):
            chunk = 1
            for df in pd.read_csv(item['path'], sep=';', dtype=str, chunksize=100000):

                if item['database'] == "candidatos":
                    self._save_candidatos(df, item, chunk)

                if item['database'] == "legendas":
                    self._save_legendas(df, item, chunk)

                chunk += 1

    def _save(self, df, item, chunk):
        folder = "dim_%s" % item['database']
        output_path = os.path.join(self.output, folder, item['name'])

        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        header = chunk == 1
        mode = 'a' if chunk > 1 else 'w+'
        df.to_csv(output_path, header=header, mode=mode, compression='gzip', sep=';', encoding='utf-8', index=False,
                  quoting=QUOTE_ALL)

    def set_ids(self, df, name, start=1):
        df.is_copy = False
        columns = [c for c in df.columns if c != name]
        df[name] = range(start, start + len(df))

        return df[[name] + columns]

    def _save_candidatos(self, df, item, chunk):
        if chunk == 1 and item['year'] == 2010:
            brancos_nulos = pd.DataFrame([
                {'NOME_CANDIDATO': 'VOTO BRANCO', 'NUMERO_CANDIDATO': '95',
                 'NOME_PARTIDO': 'VOTO BRANCO', 'NUMERO_PARTIDO': '95'},
                {'NOME_CANDIDATO': 'VOTO NULO', 'NUMERO_CANDIDATO': '96',
                 'NOME_PARTIDO': 'VOTO NULO', 'NUMERO_PARTIDO': '96'}
            ], columns=df.columns.tolist()).fillna('#NE#')
            df = brancos_nulos.append(df, ignore_index=True)

        df = self.set_ids(df, "ID_CANDIDATO", self.last_cand_id)
        self._save(df[self.candidatos], item, chunk)
        self.last_cand_id += len(df)

    def _save_legendas(self, df, item, chunk):
        if chunk == 1 and item['year'] == 2010:
            brancos_nulos = pd.DataFrame([
                {'NOME_PARTIDO': 'VOTO BRANCO', 'NUMERO_PARTIDO': '95'},
                {'NOME_PARTIDO': 'VOTO NULO', 'NUMERO_PARTIDO': '96'}
            ], columns=df.columns.tolist()).fillna('#NE#')
            df = brancos_nulos.append(df, ignore_index=True)

        df = self.set_ids(df, "ID_LEGENDA", self.last_leg_id)
        self._save(df[self.legendas], item, chunk)
        self.last_leg_id += len(df)

    def _done(self, item):
        folder = "dim_%s" % item['database']
        output_path = os.path.join(self.output, folder, item['name'])
        return os.path.exists(output_path)
