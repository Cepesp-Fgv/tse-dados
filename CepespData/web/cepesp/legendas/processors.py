from web.cepesp.legendas.options import LegendasOptions
from web.cepesp.legendas.readers import LegendasReader, NewLegendasReader

from web.cepesp.utils.data import apply_filters, apply_order_by, apply_translations


class LegendasQuery:
    def __init__(self):
        self.options = LegendasOptions()
        if (2010 in self.options.years) or (2014 in self.options.years):
            self.reader = NewLegendasReader(self.options)
        else:
            self.reader = LegendasReader(self.options)

    def get(self):
        df = self.reader.read()

        before = len(df)
        df = apply_filters(df, self.options.filters)
        after = len(df)

        df = apply_order_by(df, self.options.selected_columns, self.options.order_by_columns)
        df = apply_translations(df, self.options.selected_columns)

        return [df, before, after]
