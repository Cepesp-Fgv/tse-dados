import pandas as pd

from etl.process.DimensionProcess import DimensionsProcess


class CoalitionsProcess(DimensionsProcess):
    columns = [
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

    def get_id_column(self):
        return "ID_LEGENDA"

    def check(self, item):
        return item['database'] == "legendas"

    def get_columns(self):
        return self.columns

    def get_brancos_df(self, item, job):
        return pd.DataFrame([
            {'ANO_ELEICAO': str(item['year']), 'CODIGO_CARGO': str(job), 'NOME_PARTIDO': 'VOTO BRANCO',
             'NUMERO_PARTIDO': '95'},
            {'ANO_ELEICAO': str(item['year']), 'CODIGO_CARGO': str(job), 'NOME_PARTIDO': 'VOTO NULO',
             'NUMERO_PARTIDO': '96'}
        ], columns=self.columns).fillna('#NE#')
