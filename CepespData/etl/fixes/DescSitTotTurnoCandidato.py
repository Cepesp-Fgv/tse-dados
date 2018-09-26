import pandas as pd


class DescSitTotTurnoCandidato:

    def check(self, item):
        return item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        df.at[df["COD_SIT_TOT_TURNO"] == "-1", "DESC_SIT_TOT_TURNO"] = "#NULO#"

        df.at[df["DESC_SIT_TOT_TURNO"] == "ELEITO", "COD_SIT_TOT_TURNO"] = "1"
        df.at[df["COD_SIT_TOT_TURNO"] == "ELEITO POR QP", "COD_SIT_TOT_TURNO"] = "2"
        df.at[df["COD_SIT_TOT_TURNO"] == "ELEITO POR MÉDIA", "COD_SIT_TOT_TURNO"] = "3"
        df.at[df["COD_SIT_TOT_TURNO"] == "NÃO ELEITO", "COD_SIT_TOT_TURNO"] = "4"
        df.at[df["COD_SIT_TOT_TURNO"] == "SUPLENTE", "COD_SIT_TOT_TURNO"] = "5"
        df.at[df["COD_SIT_TOT_TURNO"] == "2º TURNO", "COD_SIT_TOT_TURNO"] = "6"

        return df

    def test(self, client):
        pass