import pandas as pd

from lib.tse.options import TSEVotosOptions
from lib.tse.readers import TSEVotosReader
from lib.utils.data import apply_filters, apply_order_by, apply_translations


class TSEVotosQuery:
    def __init__(self):
        self.options = TSEVotosOptions()
        self.reader = TSEVotosReader(self.options)

    def apply_group_by(self, df):
        columns = list(set(self.options.selected_columns) - set(self.options.sum_columns))

        for sum_c in self.options.sum_columns:
            try:
                df[sum_c] = pd.to_numeric(df[sum_c], errors='coerce')
            except KeyError:
                print("Column %s not found. (could not change to numeric)" % sum_c)

        if 'NUMERO_PARTIDO' in self.options.selected_columns and self.options.job is 1:
            df['NUMERO_PARTIDO'] = df['NUMERO_CANDIDATO']

        df = df.groupby(columns, as_index=False).sum()

        return df

    def get(self):
        df = self.reader.read()
        df = self.apply_group_by(df)

        before = len(df)
        df = apply_filters(df, self.options.filters)
        after = len(df)

        df = apply_order_by(df, self.options.selected_columns, self.options.order_by_columns)
        df = apply_translations(df, self.options.selected_columns)

        return [df, before, after]
