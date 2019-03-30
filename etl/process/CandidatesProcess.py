import pandas as pd

from etl.process.DimensionProcess import DimensionsProcess


class CandidatesProcess(DimensionsProcess):
    columns = [
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

    def get_id_column(self):
        return "ID_CANDIDATO"

    def check(self, item):
        return item['database'] == "candidatos"

    def get_columns(self):
        return self.columns

    def get_brancos_df(self, item, job):
        return pd.DataFrame([
            {'ANO_ELEICAO': str(item['year']), 'CODIGO_CARGO': str(job), 'NOME_CANDIDATO': 'VOTO BRANCO',
             'NUMERO_CANDIDATO': '95', 'NOME_PARTIDO': 'VOTO BRANCO', 'NUMERO_PARTIDO': '95'},
            {'ANO_ELEICAO': str(item['year']), 'CODIGO_CARGO': str(job), 'NOME_CANDIDATO': 'VOTO NULO', 'NUMERO_CANDIDATO': '96',
             'NOME_PARTIDO': 'VOTO NULO', 'NUMERO_PARTIDO': '96'}
        ], columns=self.columns).fillna('#NE#')
