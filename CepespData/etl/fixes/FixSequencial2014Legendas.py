import pandas as pd


class FixSequencial2014Legendas:

    def check(self, item):
        return item['year'] == 2014 and item['database'] == 'legendas' and not item['president']

    def apply(self, df: pd.DataFrame):
        df.loc[df['SEQUENCIA_COLIGACAO'] == '#NE#', 'SEQUENCIA_COLIGACAO'] = df['CODIGO_COLIGACAO']
        df.loc[df['TIPO_LEGENDA'] == 'PARTIDO ISOLADO', 'NOME_COLIGACAO'] = df['SIGLA_COLIGACAO']

        return df

    def test(self, client):
        df = client.get_legendas(year=2014, job=3, columns=['SEQUENCIAL_COLIGACAO'])
        df = df[df['TIPO_LEGENDA'] == 'PARTIDO ISOLADO']

        assert len(df[df['NOME_COLIGACAO'] == '#NE#']) == 0, "wrong NOME_COLIGACAO"
        assert len(df[df['SEQUENCIA_COLIGACAO'] == '#NE#']) == 0, "wrong SEQUENCIAL_COLIGACAO"

