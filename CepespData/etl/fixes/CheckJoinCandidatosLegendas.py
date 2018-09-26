import pandas as pd

from web.cepesp.tse.columns import TSEVotosColumnsSelector


class CheckJoinCandidatosLegendas:

    def check(self, item):
        return False

    def apply(self, df: pd.DataFrame):
        return df

    def test(self, client):
        # cand = client.get_candidates(year=2014, job=6, only_elected=True)
        # cand = cand.rename(columns={'CODIGO_LEGENDA': 'SEQUENCIAL_COLIGACAO'})
        # cand = cand.set_index(["NUMERO_PARTIDO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO", "SEQUENCIAL_COLIGACAO"])
        #
        # leg = client.get_coalitions(year=2014, job=6)
        # leg = leg.set_index(["NUMERO_PARTIDO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO", "SEQUENCIAL_COLIGACAO"])
        #
        # merged = cand.merge(leg, how="left", left_index=True, right_index=True).reset_index()
        # merged = merged.set_index(["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"])
        #
        # assert len(merged) == 513, "not 513 candidates"
        #
        # votes = client.get_votes(year=2014, job=6, regional_aggregation=0)
        # votes = votes.set_index(["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"])
        #
        # merged2 = merged.merge(votes, how="left", left_index=True, right_index=True).reset_index()
        #
        # assert len(merged2) == 513, "not 513 candidates-votes"

        columns = TSEVotosColumnsSelector(2, 0).columns()
        tse = client.get_elections(year=2014, job=6, regional_aggregation=0, political_aggregation=2, only_elected=True,
                                   columns=columns)
        count = len(tse)

        assert count == 513, "showing %d instead of 513 results" % count
