from lib.legendas.options import LegendasOptions
from lib.legendas.readers import LegendasReader

from lib.utils.data import apply_filters, apply_order_by, apply_translations


class LegendasQuery:
    def __init__(self):
        self.options = LegendasOptions()
        self.reader = LegendasReader(self.options)

    def get(self):
        df = self.reader.read()

        before = len(df)
        df = apply_filters(df, self.options.filters)
        after = len(df)

        df = apply_order_by(df, self.options.selected_columns, self.options.order_by_columns)
        df = apply_translations(df, self.options.selected_columns)

        return [df, before, after]
