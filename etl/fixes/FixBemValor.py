import pandas as pd


class FixBemValor:

    def check(self, item):
        return item['database'] == 'bem_candidato'

    def apply(self, df: pd.DataFrame):
        df['VALOR_BEM'] = df['VALOR_BEM'].str.replace(',', '.').astype(float)
        df['VALOR_BEM'] = df['VALOR_BEM'].map('{:,.2f}'.format)

        df['VALOR_BEM'] = df['VALOR_BEM'].str.replace(',', '_')  # , -> _
        df['VALOR_BEM'] = df['VALOR_BEM'].str.replace('.', ',')  # . -> ,
        df['VALOR_BEM'] = df['VALOR_BEM'].str.replace('_', '.')  # _ -> .

        return df

    def test(self, client):
        pass
