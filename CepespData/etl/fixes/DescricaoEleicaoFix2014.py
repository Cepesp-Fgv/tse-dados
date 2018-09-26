import pandas as pd


class DescricaoEleicaoFix2014:

    def __init__(self):
        self.descriptions = [
            "ELEIÇÕES GERAIS 2014",
            "Eleições Gerais 2014",
            "ELEICOES"
        ]

    def check(self, item):
        return item['year'] == 2014

    def apply(self, df: pd.DataFrame):
        for desc in self.descriptions:
            df.at[df["DESCRICAO_ELEICAO"] == desc, "DESCRICAO_ELEICAO"] = "Eleicoes Gerais 2014"

        return df

    def _count_df(self, df):
        total = 0
        for desc in self.descriptions:
            total += len(df[df['DESCRICAO_ELEICAO'] == desc])

        return total

    def test(self, client):
        for j in [1, 3, 5, 6, 7, 8]:
            cand_df = client.get_candidates(year=2014, job=j)
            legendas_df = client.get_coalitions(year=2014, job=j)
            votos_df = client.get_votes(year=2014, job=j, regional_aggregation=0,
                                        columns=['DESCRICAO_ELEICAO', 'QTDE_VOTOS'])

            assert self._count_df(cand_df) == 0, "candidatos, 2014, job %d" % j
            assert self._count_df(legendas_df) == 0, "legendas, 2014, job %d" % j
            assert self._count_df(votos_df) == 0, "votos, 2014, job %d" % j

        for j in [2, 4, 9, 10]:
            cand_df = client.get_candidates(year=2014, job=j)
            legendas_df = client.get_coalitions(year=2014, job=j)

            assert self._count_df(cand_df) == 0, "candidatos, 2014, job %d" % j
            assert self._count_df(legendas_df) == 0, "legendas, 2014, job %d" % j