import pandas as pd

from web.cepesp.tse.options import TSEVotosOptions
from web.cepesp.tse.readers import TSEVotosReader, PresidentVotosCandidatosReader, TSEDatabaseReader
from web.cepesp.utils.data import apply_filters, apply_order_by, apply_translations


class TSEVotosQuery:

    def __init__(self):
        self.options = TSEVotosOptions()

        if self.options.job == 1 and self.options.pol == 2:
            self.reader = PresidentVotosCandidatosReader(self.options)
        else:
            self.reader = TSEVotosReader(self.options)

    def apply_group_by(self, df):
        df = df.fillna('#NE#')

        columns = list(set(self.options.selected_columns) - set(self.options.sum_columns))

        for sum_c in self.options.sum_columns:
            df[sum_c] = pd.to_numeric(df[sum_c], errors='coerce')

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
