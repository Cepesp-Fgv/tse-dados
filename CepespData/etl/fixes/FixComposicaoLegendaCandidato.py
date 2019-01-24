import pandas as pd

from web.cepesp.utils.data import resolve_conflicts


class FixComposicaoLegendaCandidato2006:

    def __init__(self, leg_path, leg_presidente_path):
        self.leg_path = leg_path
        self.leg_presidente_path = leg_presidente_path

    def check(self, item):
        return item['database'] == 'candidatos' and item['year'] == 2006

    def apply(self, df):
        leg = pd.read_csv(self.leg_path, sep=';', dtype=str, low_memory=False)\
            .append(pd.read_csv(self.leg_presidente_path, sep=';', dtype=str, low_memory=False))

        idx = ["ANO_ELEICAO", "CODIGO_CARGO", "NUMERO_PARTIDO", "SIGLA_UE"]
        columns = df.columns.tolist()

        leg = leg.drop_duplicates(idx)

        before = len(df)
        df = df.set_index(idx)
        df = df.merge(leg.set_index(idx), how='left', left_index=True, right_index=True).reset_index()

        df['COMPOSICAO_LEGENDA'] = df['COMPOSICAO_COLIGACAO']
        df['CODIGO_LEGENDA'] = df['SEQUENCIA_COLIGACAO']
        df['SIGLA_LEGENDA'] = df['SIGLA_PARTIDO_y']
        df['SIGLA_PARTIDO_x'] = df['SIGLA_PARTIDO_y']
        df['NOME_COLIGACAO_x'] = df['NOME_COLIGACAO_y']
        df = resolve_conflicts(df)

        after = len(df)
        if after > before:
            raise Exception(f'Duplicating Values {after - before}')

        return df[columns]
