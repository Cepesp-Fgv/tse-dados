from flask import request
from flask_babel import gettext

from web.cepesp.candidatos.columns import CandidatosColumnsSelector
from web.cepesp.utils.data import JOBS
from web.cepesp.utils.request import get_request_years, get_selected_columns, get_request_filters


class CandidatosOptions:

    def __init__(self):
        self.job = request.args.get('cargo', 1, int)
        self.only_elected = not(not(request.args.get('only_elected')))
        self.years = get_request_years(self.job)
        self.name = 'CANDIDATOS_%s_%s' % (JOBS[self.job], "_".join(map(str, self.years)))

        selector = CandidatosColumnsSelector()
        self.all_columns = selector.columns()
        self.default_columns = selector.visible_columns()
        self.selected_columns = get_selected_columns(self.default_columns, self.all_columns)
        self.order_by_columns = selector.order_by_columns()
        self.translated_columns = [gettext('columns.' + c) for c in self.selected_columns]

        self.filters = get_request_filters(self.selected_columns)

        if self.years[0] != 2014:
            if self.job == 7:
                self.filters['CODIGO_CARGO'] = [7, 8]
            else:
                self.filters['CODIGO_CARGO'] = self.job

        if self.only_elected:
            self.filters['DESC_SIT_TOT_TURNO'] = '^(ELEITO|MEDIA|MÉDIA|ELEITO POR QP|ELEITO POR MEDIA|ELEITO POR MÉDIA)$'
