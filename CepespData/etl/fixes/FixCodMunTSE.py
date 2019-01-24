import pandas as pd


class FixCodMunTSE:

    def check(self, item):
        return item['database'] == 'votos'

    def apply(self, df: pd.DataFrame):
        df['COD_MUN_TSE'] = df['COD_MUN_TSE'].str.zfill(5)

        return df

    def test(self, client):
        pass
