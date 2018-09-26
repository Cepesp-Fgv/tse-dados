from flask import request
from flask_babel import gettext

from web.cepesp.tse.columns import TSEVotosColumnsSelector
from web.cepesp.utils.data import JOBS, REG, POL
from web.cepesp.utils.request import get_request_years, get_selected_columns, get_request_filters


class AthenaQueryOptions:

    def __init__(self):
        self.reg = request.args.get('agregacao_regional', 1, int)
        self.pol = request.args.get('agregacao_politica', 2, int)
        self.job = request.args.get('cargo', 1, int)
        self.years = get_request_years(self.job)
        self.uf_filter = request.args.get('uf_filter')
        self.mun_filter = request.args.get('mun_filter')
        self.turno = request.args.get('turno')
        self.brancos = not (not (request.args.get('brancos')))
        self.nulos = not (not (request.args.get('nulos')))
        self.turno = request.args.get('turno')
        self.only_elected = not (not (request.args.get('only_elected')))
        self.name = 'ATHENA_%s_%s_%s_%s' % (JOBS[self.job], REG[self.reg], POL[self.pol], "_".join(map(str, self.years)))

        selector = TSEVotosColumnsSelector(self.pol, self.reg)
        self.all_columns = selector.columns()
        self.default_columns = self.all_columns
        self.selected_columns = get_selected_columns(self.default_columns, self.all_columns)
        self.order_by_columns = selector.order_by_columns()
        self.translated_columns = [gettext('columns.' + c) for c in self.selected_columns]

        self.filters = get_request_filters(self.selected_columns)