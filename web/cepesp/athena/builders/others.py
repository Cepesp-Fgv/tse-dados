from web.cepesp.columns.votos import VotesColumnsSelector
from web.cepesp.athena.builders.base import AthenaBuilder
from web.cepesp.columns.candidatos import CandidatesColumnsSelector
from web.cepesp.columns.legendas import CoalitionsColumnsSelector


class CandidatesCoalitionsQueryBuilder(AthenaBuilder):

    def __init__(self, **options):
        super().__init__(**options)
        table = self.arg('table')

        if table == 'candidatos':
            self.selector = CandidatesColumnsSelector()
        elif table == 'legendas':
            self.selector = CoalitionsColumnsSelector()

    def build(self):
        table = self.arg('table')
        years = "', '".join(map(str, self.arg('years')))

        columns = ", ".join([f"{self._map_column(c)} AS {c}" for c in self.selected_columns()])
        return f'''
            SELECT {columns} FROM {table} AS v
            WHERE p_ano IN (\'{years}\') 
            AND {self._build_filter_job()}
            {self._build_filters('AND')}
            {self._build_order_by()}
        '''

    # region def _build_filters(self, start): [...]
    def _build_filters(self, start):
        where = self._build_base_filters()

        if self.opt('turno'):
            where.append(f"v.NUM_TURNO = '{self.options['turno']}'")

        if self.opt('only_elected', False) and self.arg('table') == 'candidatos':
            where.append(f"v.COD_SIT_TOT_TURNO IN ('1', '2', '3')")

        if len(where) > 0:
            return f"{start} " + "\n AND ".join(where)
        else:
            return ""
    # endregion


class VotesQueryBuilder(AthenaBuilder):

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = VotesColumnsSelector(self.arg('reg'))

    def build(self):
        table = self.table_name("votos")
        years = "', '".join(map(str, self.arg('years')))
        selected_columns = self.selected_columns()
        sum_columns = [c for c in self.selector.sum_columns() if c in selected_columns]
        columns = [c for c in self.selected_columns() if c not in sum_columns]

        sum_columns = ", ".join([f"SUM({c}) AS {c}" for c in sum_columns])
        group_columns = ", ".join(map(str, range(1, len(columns) + 1)))
        columns = ", ".join([f"{c} AS {c}" for c in columns])

        if sum_columns:
            sum_columns = ", " + sum_columns

        return f'''
            SELECT {columns}{sum_columns} 
            FROM {table}
            WHERE p_ano IN (\'{years}\') 
            AND {self._build_filter_job()}
            {self._build_filter_uf()}
            GROUP BY {group_columns}
            {self._build_filters('HAVING')}
            {self._build_order_by()}
        '''

    def _build_filter_uf(self):
        uf = self.opt('uf_filter')
        if self.arg('reg') >= 2 and uf:
            years = self.arg('years')
            if 2018 in years or 2014 in years or 2002 in years:
                return f"AND UF = '{uf}'"
            else:
                return f"AND p_uf = '{uf}'"
        else:
            return ""

    # region def _build_filters(self, start): [...]
    def _build_filters(self, start):
        where = self._build_base_filters()

        where.append("NUMERO_CANDIDATO <> '97'")

        if not self.opt('brancos', True):
            where.append("NUMERO_CANDIDATO <> '95'")

        if not self.opt('nulos', True):
            where.append("NUMERO_CANDIDATO <> '96'")

        if self.opt('mun_filter'):
            where.append(f"COD_MUN_TSE = '{self.options['mun_filter']}'")

        if self.opt('turno'):
            where.append(f"NUM_TURNO = '{self.options['turno']}'")

        if len(where) > 0:
            return f"{start} " + "\n AND ".join(where)
        else:
            return ""
    # endregion
