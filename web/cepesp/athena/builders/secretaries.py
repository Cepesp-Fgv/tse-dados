from web.cepesp.athena.builders.base import AthenaBuilder
from web.cepesp.columns.secretarios import SecretariesColumnsSelector


class SecretariesQueryBuilder(AthenaBuilder):

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = SecretariesColumnsSelector()

    def build(self):
        columns_renamed = ", ".join([f"{c} AS {c}" for c in self.selected_columns()])

        return f'''
            SELECT {columns_renamed}
            FROM secretarios
            {self._build_filters()}
            {self._build_order_by()}
        '''

    # region def _build_filters(self, start): [...]
    def _build_filters(self):
        where = self._build_base_filters()

        if self.opt('uf_filter'):
            where.append(f"UF = '{self.options['uf_filter']}'")

        if self.opt('name_filter'):
            words = self.opt('name_filter').lower().split(' ')

            for w in words:
                where.append(f"REGEXP_LIKE(LOWER(NOME_SECRETARIO), '{w}')")

        if self.opt('government_period'):
            period = self.opt('government_period').split('-')
            where.append(f"DATA_ASSUMIU <> '#NE#'")
            where.append(f"DATA_DEIXOU <> '#NE#'")
            where.append(f"DATA_ASSUMIU <> ''")
            where.append(f"DATA_DEIXOU <> ''")
            if len(period) > 1:
                where.append(f"CAST(SUBSTR(DATA_ASSUMIU, 1, 4) as integer) > {period[0]}")
                where.append(f"CAST(SUBSTR(DATA_DEIXOU, 1, 4) as integer) <= {period[1]}")
            else:
                where.append(f"CAST(SUBSTR(DATA_ASSUMIU, 1, 4) as integer) = {period[0]}")

        if len(where) > 0:
            return f"WHERE " + "\n AND ".join(where)
        else:
            return ""
