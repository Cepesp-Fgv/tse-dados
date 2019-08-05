from web.cepesp.athena.builders.base import AthenaBuilder
from web.cepesp.columns.filiados import PartyAffiliationsColumnsSelector


class PartyAffiliationsQueryBuilder(AthenaBuilder):

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = PartyAffiliationsColumnsSelector()

    def build(self):
        columns_renamed = ", ".join([f"{c} AS {c}" for c in self.selected_columns()])

        return f'''
            SELECT {columns_renamed}
            FROM filiados
            WHERE {self._build_filter_party()} AND {self._build_filter_uf()}
            {self._build_filters('AND')}
            {self._build_order_by()}
        '''

    def _build_filter_uf(self):
        uf = self.opt('uf_filter')
        if uf:
            return f"p_uf = '{uf}'"
        else:
            return ""

    def _build_filter_party(self):
        party = self.opt('party')
        if party:
            party = party.lower().replace(' ', '_')
            return f"p_partido = '{party}'"
        else:
            return ""

    # region def _build_filters(self, start): [...]
    def _build_filters(self, start):
        where = self._build_base_filters()

        if self.opt('mun_filter'):
            where.append(f"COD_MUN_TSE = '{self.options['mun_filter']}'")

        if self.opt('turno'):
            where.append(f"NUM_TURNO = '{self.options['turno']}'")

        if len(where) > 0:
            return f"{start} " + "\n AND ".join(where)
        else:
            return ""
    # endregion
