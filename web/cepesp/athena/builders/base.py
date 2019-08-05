from web.cepesp.utils.request import escape
from web.cepesp.utils.data import guess_match_type
from web.cepesp.athena.builders.utils import opt, arg


class AthenaBuilder:
    int_columns = ['ID_CANDIDATO', 'ID_LEGENDA', 'v.ID_CANDIDATO', 'v.ID_LEGENDA']

    def __init__(self, **options):
        self.options = options
        self.selector = None

    def opt(self, key, default=None):
        return opt(self.options, key, default)

    def arg(self, key):
        return arg(self.options, key)

    # region Options
    def selected_columns(self):
        selected = self.opt('selected_columns', [])
        all_columns = self.columns()
        if len(selected) == 0:
            return all_columns
        else:
            return [c for c in selected if c in all_columns]

    def table_name(self, prefix):
        reg = self.arg('reg')
        if reg == 9:
            return f"{prefix}_votsec"
        elif reg == 8:
            return f"{prefix}_zona"
        elif reg == 7:
            return f"{prefix}_munzona"
        elif reg == 6:
            return f"{prefix}_mun"
        elif reg == 5:
            return f"{prefix}_micro"
        elif reg == 4:
            return f"{prefix}_meso"
        else:
            return f"{prefix}_uf"

    def columns(self):
        return self.selector.columns()

    # endregion

    # region Custom Statement Builders
    def _map_column(self, column):
        return column

    def _build_filter_job(self):
        job = self.arg('job')
        if job == 7:
            return "(p_cargo = '7' OR p_cargo = '8')"
        else:
            return f"(p_cargo = '{job}')"

    def _build_order_by(self):
        selected = self.selected_columns()
        order_by = [f"{self._map_column(c)} ASC" for c in self.selector.order_by_columns() if c in selected]

        if len(order_by) > 0:
            order_by = ", ".join(order_by)
            return f"ORDER BY {order_by}"
        else:
            return ""

    def _build_base_filters(self):
        filters = self.opt('filters', {})
        columns = self.columns()

        where = []
        for column, value in filters.items():
            if value and column in columns:
                match_type = guess_match_type(value)
                column = self._map_column(column)
                value = escape(value)

                if column in self.int_columns:
                    where.append(f"{column} = {value}")
                if match_type == "int":
                    where.append(f"{column} = '{value}'")
                elif match_type == "list":
                    value = "', '".join(value)
                    where.append(f"{column} IN ('{value}')")
                else:
                    value = str(value).lower()
                    where.append(f"REGEXP_LIKE(LOWER({column}), '{value}')")

        return where

    # endregion

    def build(self):
        raise NotImplemented()
