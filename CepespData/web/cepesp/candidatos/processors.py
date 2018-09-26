from web.cepesp.candidatos.options import CandidatosOptions
from web.cepesp.candidatos.readers import CandidatosReader, NewCandidatosReader
from web.cepesp.utils.data import apply_filters, apply_order_by, apply_translations


class CandidatosQuery:
    def __init__(self):
        self.options = CandidatosOptions()
        if (2010 in self.options.years) or (2014 in self.options.years):
            self.reader = NewCandidatosReader(self.options)
        else:
            self.reader = CandidatosReader(self.options)

    def get(self):
        df = self.reader.read()

        before = len(df)
        df = apply_filters(df, self.options.filters)
        after = len(df)

        df = apply_order_by(df, self.options.selected_columns, self.options.order_by_columns)
        df = apply_translations(df, self.options.selected_columns)

        return [df, before, after]
