import pandas as pd


class FixTituloEleitor:
    titulo = 'NUM_TITULO_ELEITORAL_CANDIDATO'
    cpf = 'CPF_CANDIDATO'

    def check(self, item):
        return item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        df.at[df[self.titulo] != '#NULO#', self.titulo] = df[self.titulo].str.zfill(12)
        df.at[df[self.cpf] != '#NULO#', self.cpf] = df[self.cpf].str.zfill(11)

        return df

    def test(self, client):
        pass
