from flask import request
from flask_babel import gettext

from web.cepesp.tse.columns import TSEVotosColumnsSelector
from web.cepesp.utils.data import JOBS, REG, POL
from web.cepesp.utils.request import get_request_years, get_selected_columns, get_request_filters


class TSEVotosOptions:
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
        self.name = 'TSE_%s_%s_%s_%s' % (JOBS[self.job], REG[self.reg], POL[self.pol], "_".join(map(str, self.years)))

        selector = TSEVotosColumnsSelector(self.pol, self.reg)
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

        candidatos = request.args.get("candidatos")
        if candidatos:
            self.filters['NUMERO_CANDIDATO'] = [int(c) for c in candidatos.split(',')]

        partidos = request.args.get("partidos")
        if partidos:
            self.filters['NUMERO_PARTIDO'] = [int(p) for p in partidos.split(',')]

        if self.only_elected:
            self.filters['DESC_SIT_TOT_TURNO'] = '^(ELEITO|MEDIA|MÉDIA|ELEITO POR QP|ELEITO POR MEDIA|ELEITO POR MÉDIA)$'
