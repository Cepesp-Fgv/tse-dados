import pandas as pd


class FixEmailCandidato:

    def check(self, item):
        return item['database'] == 'candidatos' and item['year'] <= 2010

    def apply(self, df: pd.DataFrame):
        df["EMAIL_CANDIDATO"] = "#NE#"

        return df

    def test(self, client):
        pass
