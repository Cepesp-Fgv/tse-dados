import pandas as pd


class AppendExtraJobs2014:

    def __init__(self, candidatos_2014_semvotos):
        self.candidatos = pd.read_csv(candidatos_2014_semvotos, sep=';', dtype=str, low_memory=False)

    def check(self, item):
        return item['year'] == 2014 and item['database'] == 'candidatos'

    def apply(self, df):
        df = df.append(self.candidatos, ignore_index=True, verify_integrity=True)

        return df

    def test(self, client):
        df_2 = client.get_candidates(year=2014, job=2)
        df_4 = client.get_candidates(year=2014, job=4)
        df_9 = client.get_candidates(year=2014, job=9)
        df_10 = client.get_candidates(year=2014, job=10)

        assert len(df_2) > 0, "empty vice-president"
        assert len(df_4) > 0, "empty vice-governor"
        assert len(df_9) > 0, "empty 1st substitute"
        assert len(df_10) > 0, "empty 2st substitute"
