import re

from flask import request
from flask_babel import gettext

from web.cepesp.columns.bem_candidato import BemCandidatoColumnsSelector
from web.cepesp.columns.candidatos import CandidatosColumnsSelector
from web.cepesp.columns.legendas import LegendasColumnsSelector
from web.cepesp.columns.tse import TSEVotosColumnsSelector
from web.cepesp.columns.votos import VotosMunColumnsSelector
from werkzeug.exceptions import BadRequest

from web.cepesp.utils.data import JOBS, REG, POL
from web.cepesp.utils.request import get_request_years, get_selected_columns, get_request_filters


class AthenaQueryOptions:

    def __init__(self, table=None):
        self.table = request.args.get('table') if table is None else table
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
        self.start = request.args.get("start", 0, int)
        self.length = request.args.get("length", -1, int)
        self.separator = request.args.get('sep', ',')
        self.format = request.args.get('format', 'csv')

        if self.table == 'tse':
            self.name = 'TSE_%s_%s_%s_%s' % (
                JOBS[self.job], REG[self.reg], POL[self.pol], "_".join(map(str, self.years)))
            selector = TSEVotosColumnsSelector(self.pol, self.reg)
        elif self.table == 'votos':
            self.name = 'VOTOS_%s_%s_%s' % (JOBS[self.job], REG[self.reg], "_".join(map(str, self.years)))
            selector = VotosMunColumnsSelector(self.reg)
        elif self.table == 'candidatos' :
            self.name = 'CANDIDATOS_%s_%s' % (JOBS[self.job], "_".join(map(str, self.years)))
            selector = CandidatosColumnsSelector()
        elif self.table == 'legendas':
            self.name = 'LEGENDAS_%s_%s' % (JOBS[self.job], "_".join(map(str, self.years)))
            selector = LegendasColumnsSelector()
        elif self.table == 'bem_candidato':
            self.name = 'BEM_CANDIDATO_%s' % ("_".join(map(str, self.years)))
            selector = BemCandidatoColumnsSelector()
        else:
            raise BadRequest(f'Invalid table {self.table} supplied')

        self.all_columns = selector.columns()
        self.default_columns = selector.visible_columns()
        self.selected_columns = get_selected_columns(self.default_columns, self.all_columns)
        self.order_by_columns = selector.order_by_columns()
        self.translated_columns = [gettext('columns.' + c) for c in self.selected_columns]

        self.filters = get_request_filters(self.selected_columns)

    def to_dict(self):
        return self.__dict__


class AthenaResultOptions:

    def __init__(self):
        self.query_id = str(request.args.get('id')).lower()
        self.start = request.args.get("start", 0, int)
        self.length = request.args.get("length", -1, int)
        self.separator = request.args.get('sep', ',')
        self.format = request.args.get('format', 'csv')

    def validate(self):
        if not re.match('[\-0-9a-f]+', self.query_id):
            raise BadRequest('Invalid ID Provided')

    def to_dict(self):
        return self.__dict__
