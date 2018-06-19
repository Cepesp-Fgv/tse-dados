import pandas as pd

from lib.utils.data import apply_filters, apply_order_by, apply_translations
from lib.utils.mun import read_aux_mun_code
from lib.votos.options import VotosMunOptions
from lib.votos.readers import VotosMunReader


class VotosMunQuery:
    def __init__(self):
        self.options = VotosMunOptions()
        self.reader = VotosMunReader(self.options)

    def apply_joins(self, df):
        if self.options.reg == 9:
            mun_df = read_aux_mun_code()
            mun_df = mun_df[mun_df['SIGLA_UF'] == self.options.uf_filter]
            df = df.merge(mun_df, on='COD_MUN_TSE', how='left', sort=False)
            df = df.rename(
                columns={'SIGLA_UF_x': 'UF', 'NOME_MUNICIPIO_y': 'NOME_MUNICIPIO', 'NUM_VOTAVEL': 'NUMERO_CANDIDATO'})

        return df

    def apply_group_by(self, df):
        if self.options.reg == 9:
            return df

        columns = list(set(self.options.all_columns) - set(self.options.sum_columns))
        df.QTDE_VOTOS = pd.to_numeric(df['QTDE_VOTOS'], errors='coerce')

        df = df.groupby(columns, as_index=False).sum()

        return df

    def get(self):
        df = self.reader.read()
        df = self.apply_joins(df)
        df = self.apply_group_by(df)

        before = len(df)
        df = apply_filters(df, self.options.filters)
        after = len(df)

        df = apply_order_by(df, self.options.selected_columns, self.options.order_by_columns)
        df = apply_translations(df, self.options.selected_columns)

        return [df, before, after]
