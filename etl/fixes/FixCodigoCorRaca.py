import pandas as pd


class FixCodigoCorRaca:

    def check(self, item):
        return item['database'] == 'candidatos' and item['year'] < 2014

    def apply(self, df: pd.DataFrame):
        df["CODIGO_COR_RACA"] = "-1"
        df["DESCRICAO_COR_RACA"] = "#NE#"

        return df

    def test(self, client):
        df_2010 = client.get_candidates(year=2010, job=1, columns=['CODIGO_COR_RACA', 'DESCRICAO_COR_RACA'])
        df_2006 = client.get_candidates(year=2006, job=1, columns=['CODIGO_COR_RACA', 'DESCRICAO_COR_RACA'])
        df_2002 = client.get_candidates(year=2002, job=1, columns=['CODIGO_COR_RACA', 'DESCRICAO_COR_RACA'])
        df_1998 = client.get_candidates(year=1998, job=1, columns=['CODIGO_COR_RACA', 'DESCRICAO_COR_RACA'])

        assert "CODIGO_COR_RACA" in df_2010.columns, "CODIGO_COR_RACA not in 2010"
        assert "CODIGO_COR_RACA" in df_2006.columns, "CODIGO_COR_RACA not in 2006"
        assert "CODIGO_COR_RACA" in df_2002.columns, "CODIGO_COR_RACA not in 2002"
        assert "CODIGO_COR_RACA" in df_1998.columns, "CODIGO_COR_RACA not in 1998"

        assert "DESCRICAO_COR_RACA" in df_2010.columns, "DESCRICAO_COR_RACA not in 2010"
        assert "DESCRICAO_COR_RACA" in df_2006.columns, "DESCRICAO_COR_RACA not in 2006"
        assert "DESCRICAO_COR_RACA" in df_2002.columns, "DESCRICAO_COR_RACA not in 2002"
        assert "DESCRICAO_COR_RACA" in df_1998.columns, "DESCRICAO_COR_RACA not in 1998"
