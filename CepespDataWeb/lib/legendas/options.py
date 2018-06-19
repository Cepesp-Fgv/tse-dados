from flask import request
from flask_babel import gettext

from lib.legendas.columns import LegendasColumnsSelector
from lib.utils.data import JOBS
from lib.utils.request import get_request_years, get_selected_columns, get_request_filters


class LegendasOptions:
    def __init__(self):
        self.job = request.args.get('cargo', 1, int)
        self.years = get_request_years(self.job)
        self.name = 'LEGENDAS_%s_%s' % (JOBS[self.job], "_".join(map(str, self.years)))

        selector = LegendasColumnsSelector()
        self.all_columns = selector.columns()
        self.default_columns = selector.visible_columns()
        self.selected_columns = get_selected_columns(self.default_columns, self.all_columns)
        self.order_by_columns = selector.order_by_columns()
        self.translated_columns = [gettext('columns.' + c) for c in self.selected_columns]

        self.filters = get_request_filters(self.selected_columns)

        if self.job == 7:
            self.filters['CODIGO_CARGO'] = [7, 8]
        else:
            self.filters['CODIGO_CARGO'] = self.job
