from flask import request
from flask_babel import gettext

from lib.utils.data import JOBS, REG
from lib.utils.request import get_request_years, get_selected_columns, get_request_filters
from lib.votos.columns import VotosMunColumnsSelector


class VotosMunOptions:
    def __init__(self):
        self.reg = request.args.get('agregacao_regional', 1, int)
        self.job = request.args.get('cargo', 1, int)
        self.years = get_request_years(self.job)
        self.uf_filter = request.args.get('uf_filter')
        self.mun_filter = request.args.get('mun_filter')
        self.turno = request.args.get('turno')
        self.name = 'VOTOS_%s_%s_%s' % (JOBS[self.job], REG[self.reg], "_".join(map(str, self.years)))

        selector = VotosMunColumnsSelector(self.reg)
        self.all_columns = selector.columns()
        self.default_columns = selector.visible_columns()
        self.selected_columns = get_selected_columns(self.default_columns, self.all_columns)
        self.sum_columns = selector.sum_columns()
        self.order_by_columns = selector.order_by_columns()
        self.translated_columns = [gettext('columns.' + c) for c in self.selected_columns]

        self.filters = get_request_filters(self.selected_columns)

        if self.mun_filter:
            self.filters['COD_MUN_TSE'] = str(self.mun_filter)

        if self.uf_filter and self.reg != 9:
            self.filters['UF'] = str(self.uf_filter)

        if self.turno:
            self.filters['NUM_TURNO'] = int(self.turno)
