import pandas as pd

from web.cepesp.utils.data import resolve_conflicts


class FixSequenciaColigacao2010:

    columns = [
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

    def __init__(self, cand_2010_path):
        self.cand_2010_path = cand_2010_path
        self.idx = ['ANO_ELEICAO', 'NUM_TURNO', 'CODIGO_CARGO', 'NUMERO_PARTIDO']

    def check(self, item):
        return item['year'] == 2010 and item['database'] == 'legendas'

    def apply(self, df: pd.DataFrame):
        if len(df[df['CODIGO_CARGO'] == '1']) > 0:
            cand = pd.read_csv(self.cand_2010_path, sep=';', dtype=str).set_index(self.idx)
            df = df.set_index(self.idx)
            df = df.merge(cand, left_index=True, right_index=True).reset_index()
            df = resolve_conflicts(df)
            df['SEQUENCIA_COLIGACAO'] = df['CODIGO_LEGENDA']
            df = df[self.columns]

        return df

    def test(self, client):
        df = client.get_coalitions(year=2010, job=1, columns=['SEQUENCIAL_COLIGACAO'])
        df.SEQUENCIAL_COLIGACAO = pd.to_numeric(df['SEQUENCIAL_COLIGACAO'], errors='coerce')

        assert len(df[df['SEQUENCIAL_COLIGACAO'] > 0][df['SEQUENCIAL_COLIGACAO'] < 10000]) == 0, "wrong SEQUENCIAL_COLIGACAO"
