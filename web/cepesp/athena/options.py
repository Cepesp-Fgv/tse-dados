import re

from flask_babel import gettext

from web.cepesp.columns.filiados import PartyAffiliationsColumnsSelector
from web.cepesp.columns.bem_candidato import CandidateAssetsColumnsSelector
from web.cepesp.columns.candidatos import CandidatesColumnsSelector
from web.cepesp.columns.legendas import CoalitionsColumnsSelector
from web.cepesp.columns.tse import ElectionsColumnsSelector
from web.cepesp.columns.votos import VotesColumnsSelector
from web.cepesp.columns.secretarios import SecretariesColumnsSelector
from werkzeug.exceptions import BadRequest

from web.cepesp.utils.data import JOBS, REG, POL
from web.cepesp.utils.request import get_request_years, get_selected_columns, get_request_filters, request_get, \
    request_get_list


class AthenaQueryOptions:

    def __init__(self, table=None):
        self.table = request_get('table') if table is None else table
        self.reg = request_get('agregacao_regional', 0, int)
        self.pol = request_get('agregacao_politica', 2, int)
        self.job = request_get('cargo', 1, int)
        self.jobs = request_get_list('cargo', int)
        self.years = get_request_years(self.job) if self.table != 'filiados' else None
        self.uf_filter = request_get('uf_filter', request_get('uf'))
        self.mun_filter = request_get('mun_filter', request_get('mun'))
        self.turno = request_get('turno')
        self.brancos = not (not (request_get('brancos')))
        self.nulos = not (not (request_get('nulos')))
        self.turno = request_get('turno')
        self.only_elected = not (not (request_get('only_elected')))
        self.start = request_get("start", 0, int)
        self.length = request_get("length", -1, int)
        self.separator = request_get('sep', ',')
        self.format = request_get('format', 'csv')
        self.party = request_get('party')
        self.name_filter = request_get('name_filter', '')
        self.government_period = request_get('government_period', '')

        if self.table == 'filiados' and not (self.party and self.uf_filter):
            self.party = 'avante'
            self.uf_filter = 'ac'

        (self.name, selector) = self.get_selector()

        if self.table == 'filiados' and not (self.party or self.uf_filter):
            raise BadRequest(f'Filiados require PARTY and UF')

        self.all_columns = selector.columns()
        self.default_columns = selector.visible_columns()
        self.selected_columns = get_selected_columns(self.default_columns, self.all_columns)
        self.order_by_columns = selector.order_by_columns()
        self.translated_columns = [gettext('columns.' + c) for c in self.selected_columns]

        self.filters = get_request_filters(self.selected_columns)

    def get_selector(self):
        if self.table == 'tse':
            name = 'TSE_%s_%s_%s_%s' % (JOBS[self.job], REG[self.reg], POL[self.pol], "_".join(map(str, self.years)))
            selector = ElectionsColumnsSelector(self.pol, self.reg)
        elif self.table == 'votos':
            name = 'VOTOS_%s_%s_%s' % (JOBS[self.job], REG[self.reg], "_".join(map(str, self.years)))
            selector = VotesColumnsSelector(self.reg)
        elif self.table == 'candidatos':
            name = 'CANDIDATOS_%s_%s' % (JOBS[self.job], "_".join(map(str, self.years)))
            selector = CandidatesColumnsSelector()
        elif self.table == 'legendas':
            name = 'LEGENDAS_%s_%s' % (JOBS[self.job], "_".join(map(str, self.years)))
            selector = CoalitionsColumnsSelector()
        elif self.table == 'bem_candidato':
            name = 'BEM_CANDIDATO_%s' % ("_".join(map(str, self.years)))
            selector = CandidateAssetsColumnsSelector()
        elif self.table == 'filiados':
            name = 'FILIADOS_%s' % ("_".join([str(self.party), str(self.uf_filter)]))
            selector = PartyAffiliationsColumnsSelector()
        elif self.table == 'secretarios':
            name = 'SECRETARIOS'
            selector = SecretariesColumnsSelector()
        else:
            raise BadRequest(f'Invalid table {self.table} supplied')

        return name, selector

    def to_dict(self):
        return self.__dict__


class AthenaResultOptions:

    def __init__(self):
        self.query_id = str(request_get('id')).lower()
        self.start = request_get("start", 0, int)
        self.length = request_get("length", -1, int)
        self.separator = request_get('sep', ',')
        self.format = request_get('format', 'csv')

    def validate(self):
        if not re.match('[\-0-9a-f]+', self.query_id):
            raise BadRequest('Invalid ID Provided')

    def to_dict(self):
        return self.__dict__
