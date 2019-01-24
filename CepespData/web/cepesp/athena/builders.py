import re

from web.cepesp.columns.candidatos import CandidatosColumnsSelector
from web.cepesp.columns.legendas import LegendasColumnsSelector
from web.cepesp.columns.tse import TSEVotosColumnsSelector
from web.cepesp.columns.votos import VotosMunColumnsSelector
from web.cepesp.utils.data import guess_match_type


class Builder:

    def __init__(self, **options):
        self.options = options
        self.rx = re.compile(r'[!?\\/\-\&\*\%\$\#\"\']+', flags=re.M | re.I)

    def trim(self, value):
        return re.sub('(\r|\n| )+', ' ', value).strip()

    def escape(self, value):
        return self.rx.sub('', value)

    def opt(self, key, default=None):
        return self.options[key] if key in self.options else \
            default

    def arg(self, key):
        if key not in self.options:
            raise KeyError(f'No argument {key} supplied')

        return self.options[key]

    def votes_table(self):
        reg = self.arg('reg')
        if reg == 9:
            return "votos_votsec"
        elif reg == 8:
            return "votos_zona"
        elif reg == 7:
            return "votos_munzona"
        elif reg == 6:
            return "votos_mun"
        elif reg == 5:
            return "votos_micro"
        elif reg == 4:
            return "votos_meso"
        else:
            return "votos_uf"

    def columns(self):
        return []

    def selected_columns(self):
        selected = self.opt('selected_columns', [])
        all_columns = self.columns()
        if len(selected) == 0:
            return all_columns
        else:
            return [c for c in selected if c in all_columns]


class AthenaBuilder(Builder):

    def build(self):
        table = self.arg('table')
        if table == 'tse' and self.arg('pol') != 4:
            builder = TSEQueryBuilder(**self.options)
        elif table in ['candidatos', 'legendas', 'votos'] or self.arg('pol') == 4:
            builder = DimQueryBuilder(**self.options)
        else:
            raise KeyError(f'Invalid table {table} supplied')

        return builder.build()


class DimQueryBuilder(Builder):

    int_columns = ['ID_CANDIDATO', 'ID_LEGENDA']

    def __init__(self, **options):
        super().__init__(**options)

        table = self.arg('table')
        if table == 'candidatos':
            self.selector = CandidatosColumnsSelector()
        elif table == 'legendas':
            self.selector = LegendasColumnsSelector()
        elif table == 'votos':
            self.selector = VotosMunColumnsSelector(self.arg('reg'))
        elif table == 'tse':
            self.selector = TSEVotosColumnsSelector(4, self.arg('reg'))
        else:
            raise KeyError(f'Invalid table {table} supplied')

    def columns(self):
        return self.selector.columns()

    def build(self):
        table = self._table_name()
        years = "', '".join(map(str, self.arg('years')))

        if table.startswith('votos') or table.startswith('tse'):
            columns = set(self.selected_columns()) - set(self.selector.sum_columns())
            columns_renamed = ", ".join([f"{c} AS {c}" for c in columns])
            sum_columns = ", ".join([f"SUM({c}) AS {c}" for c in self.selector.sum_columns()])
            group_columns = ", ".join(map(str, range(1, len(columns) + 1)))
            query = f'''
                SELECT {columns_renamed}, {sum_columns} FROM {table}
                WHERE p_ano IN (\'{years}\') 
                AND {self._build_filter_job()}
                {self._build_filter_uf()}
                GROUP BY {group_columns}
                {self._build_filters('HAVING')}
                {self._build_order_by()}
            '''
        else:
            columns = ", ".join([f"{c} AS {c}" for c in self.selected_columns()])
            query = f'''
                SELECT {columns} FROM {table}
                WHERE p_ano IN (\'{years}\') 
                AND {self._build_filter_job()}
                {self._build_filter_uf()}
                {self._build_filters('AND')}
                {self._build_order_by()}
            '''

        return self.trim(query)

    def _build_order_by(self):
        selected = self.selected_columns()
        order_by = [f"{c} ASC" for c in self.selector.order_by_columns() if c in selected]

        if len(order_by) > 0:
            order_by = ", ".join(order_by)
            return f"ORDER BY {order_by}"
        else:
            return ""

    def _table_name(self):
        table = self.arg('table')
        if table == 'votos':
            return self.votes_table()
        if table == 'tse':
            return 'tse_detalhe'
        else:
            return table

    def _build_filter_uf(self):
        uf = self.opt('uf_filter')
        if uf and self.arg('table') == 'votos' and self.arg('reg') >= 2:
            years = self.arg('years')
            if 2018 in years or 2014 in years or 2002 in years:
                return f"AND UF = '{uf}'"
            else:
                return f"AND p_uf = '{uf}'"
        else:
            return ""

    def _build_filter_job(self):
        job = self.arg('job')
        if job == 7:
            return "(p_cargo = '7' OR p_cargo = '8')"
        else:
            return f"p_cargo = '{job}'"

    def _build_filters(self, start):
        filters = self.opt('filters', {})
        columns = self.columns()

        where = []
        for column, value in filters.items():
            if value and column in columns:
                match_type = guess_match_type(value)
                value = self.escape(value)
                if column in self.int_columns:
                    where.append(f"{column} = {value}")
                elif match_type == "int":
                    where.append(f"{column} = '{value}'")
                elif match_type == "list":
                    value = "', '".join(value)
                    where.append(f"{column} IN ('{value}')")
                else:
                    value = str(value).lower()
                    where.append(f"REGEXP_LIKE(LOWER({column}), '{value}')")

        if self.arg('table') == 'votos':
            if not self.opt('brancos', True):
                where.append("NUMERO_CANDIDATO <> '95'")

            if not self.opt('nulos', True):
                where.append("NUMERO_CANDIDATO <> '96'")

            if self.opt('mun_filter'):
                where.append(f"COD_MUN_TSE = '{self.options['mun_filter']}'")

        if self.opt('turno'):
            where.append(f"NUM_TURNO = '{self.options['turno']}'")

        if self.opt('only_elected', False) and self.arg('table') == 'candidatos':
            where.append(f"COD_SIT_TOT_TURNO IN ('1', '2', '3')")

        if len(where) > 0:
            return f"{start} " + "\n AND ".join(where)
        else:
            return ""


class TSEQueryBuilder(Builder):
    # <editor-fold desc="Columns" defaultstate="collapsed">
    votos = {

        # BR
        0: [
            "ANO_ELEICAO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS",
        ],

        # MACRO
        1: [
            "ANO_ELEICAO",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ],

        # UF
        2: [
            "ANO_ELEICAO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ],

        # MESO
        4: [
            "ANO_ELEICAO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ],

        # MICRO
        5: [
            "ANO_ELEICAO",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ],

        # MUNICIPIO
        6: [
            "ANO_ELEICAO",
            "COD_MUN_TSE",
            "COD_MUN_IBGE",
            "NOME_MUNICIPIO",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ],

        # MUNZONA
        7: [
            "ANO_ELEICAO",
            "NUM_ZONA",
            "COD_MUN_TSE",
            "COD_MUN_IBGE",
            "NOME_MUNICIPIO",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ],

        # ZONA
        8: [
            "ANO_ELEICAO",
            "NUM_ZONA",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ],

        # VOTACAO SECAO
        9: [
            "ANO_ELEICAO",
            "NUM_SECAO",
            "NUM_ZONA",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "CODIGO_MESO",
            "NOME_MESO",
            "UF",
            "NOME_UF",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "COD_MUN_TSE",
            "COD_MUN_IBGE",
            "NOME_MUNICIPIO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ]

    }

    candidatos = [
        'SIGLA_UE',
        'DESCRICAO_UE',
        'NOME_CANDIDATO',
        'CPF_CANDIDATO',
        'NOME_URNA_CANDIDATO',
        'COD_SITUACAO_CANDIDATURA',
        'DES_SITUACAO_CANDIDATURA',
        'CODIGO_LEGENDA',
        'SIGLA_LEGENDA',
        'COMPOSICAO_LEGENDA',
        'CODIGO_OCUPACAO',
        'DESCRICAO_OCUPACAO',
        'DATA_NASCIMENTO',
        'NUM_TITULO_ELEITORAL_CANDIDATO',
        'IDADE_DATA_ELEICAO',
        'CODIGO_SEXO',
        'DESCRICAO_SEXO',
        'COD_GRAU_INSTRUCAO',
        'DESCRICAO_GRAU_INSTRUCAO',
        'CODIGO_ESTADO_CIVIL',
        'DESCRICAO_ESTADO_CIVIL',
        'CODIGO_COR_RACA',
        'DESCRICAO_COR_RACA',
        'CODIGO_NACIONALIDADE',
        'DESCRICAO_NACIONALIDADE',
        'SIGLA_UF_NASCIMENTO',
        'CODIGO_MUNICIPIO_NASCIMENTO',
        'NOME_MUNICIPIO_NASCIMENTO',
        'DESPESA_MAX_CAMPANHA',
        'COD_SIT_TOT_TURNO',
        'DESC_SIT_TOT_TURNO',
        'EMAIL_CANDIDATO',
    ]

    legendas = [
        "TIPO_LEGENDA",
        "SIGLA_PARTIDO",
        "NOME_PARTIDO",
        'NUMERO_PARTIDO',
        "SIGLA_COLIGACAO",
        "NOME_COLIGACAO",
        "COMPOSICAO_COLIGACAO",
        "SEQUENCIA_COLIGACAO"
    ]

    int_columns = [
        'v.ID_CANDIDATO',
        'v.ID_LEGENDA'
    ]
    # </editor-fold>

    def columns(self):
        return TSEVotosColumnsSelector(self.arg('pol'), self.arg('reg')).columns()

    def build(self):
        reg = self.arg('reg')
        years = "', '".join(map(str, self.arg('years')))

        columns = ", ".join(set(self.votos[reg] + ['ID_CANDIDATO']) - {'QTDE_VOTOS'})
        group_columns = ", ".join(map(str, range(1, len(self.votos[reg]) + 1)))
        inner_query = f'''
            SELECT {columns},
                MAX(ID_LEGENDA) AS ID_LEGENDA, 
                SUM(QTDE_VOTOS) AS QTDE_VOTOS
            FROM {self.votes_table()}
            WHERE {self._build_filter_job()}
            AND p_ano IN (\'{years}\')
            {self._build_filter_uf()}
            GROUP BY {group_columns}
        '''

        columns = ", ".join(self._get_outer_query_columns())
        outer_query = f'''
            SELECT {columns}
            FROM ({inner_query}) as v
            LEFT JOIN candidatos as c ON v.ID_CANDIDATO = c.ID_CANDIDATO AND v.ANO_ELEICAO = c.ANO_ELEICAO
            LEFT JOIN legendas as l ON v.ID_LEGENDA = l.ID_LEGENDA AND v.ANO_ELEICAO = c.ANO_ELEICAO
            {self._build_where()}
            {self._build_order_by()}
        '''

        return self.trim(outer_query)

    def _get_outer_query_columns(self):
        def nome_candidato_replace(c):
            if c == "c.NOME_CANDIDATO AS NOME_CANDIDATO":
                nulo = "IF(v.NUMERO_CANDIDATO = '96', 'VOTO NULO', c.NOME_CANDIDATO)"
                return f"IF(v.NUMERO_CANDIDATO = '95', 'VOTO BRANCO', {nulo}) AS NOME_CANDIDATO"
            else:
                return c

        columns = map(lambda c: self._map_column(c, rename=True), self.selected_columns())
        columns = map(nome_candidato_replace, columns)

        return columns

    def _build_filter_job(self):
        job = self.arg('job')
        if job == 7:
            return "(p_cargo = '7' OR p_cargo = '8')"
        else:
            return f"(p_cargo = '{job}')"

    def _build_filter_uf(self):
        uf = self.opt('uf_filter')
        if uf and self.arg('reg') >= 2:
            years = self.arg('years')
            if 2018 in years or 2014 in years or 2002 in years:
                return f"AND UF = '{uf}'"
            else:
                return f"AND p_uf = '{uf}'"
        else:
            return ""

    def _build_order_by(self):
        selected = self.selected_columns()
        order_by = ['UF', 'NUM_ZONA', 'NUM_TURNO', 'SIGLA_PARTIDO', 'NOME_CANDIDATO', 'COMPOSICAO_COLIGACAO',
                    'COMPOSICAO_COLIGACAO', 'COD_MUN_IBGE']
        order_by = [f"{self._map_column(c)} ASC" for c in order_by if c in selected]

        if len(order_by) > 0:
            order_by = ", ".join(order_by)
            return f"ORDER BY {order_by}"
        else:
            return ""

    def _map_column(self, column, rename=False):
        reg = self.options['reg']
        if rename:
            if column in (self.votos[reg] + ['ID_CANDIDATO', 'ID_LEGENDA']):
                return f"v.{column} AS {column}"
            elif column in self.candidatos:
                return f"c.{column} AS {column}"
            elif column in self.legendas:
                return f"l.{column} AS {column}"
            else:
                return column
        else:
            if column in (self.votos[reg] + ['ID_CANDIDATO', 'ID_LEGENDA']):
                return f"v.{column}"
            elif column in self.candidatos:
                return f"c.{column}"
            elif column in self.legendas:
                return f"l.{column}"
            else:
                return column

    def _build_where(self):
        filters = self.opt('filters', {})
        columns = self.columns()

        where = []
        for column, value in filters.items():
            if value and column in columns:
                match_type = guess_match_type(value)
                column = self._map_column(column)
                value = self.escape(value)
                if column in self.int_columns:
                    where.append(f"{column} = {value}")
                elif match_type == "int":
                    where.append(f"{column} = '{value}'")
                elif match_type == "list":
                    value = "', '".join(value)
                    where.append(f"{column} IN ('{value}')")
                else:
                    value = str(value).lower()
                    where.append(f"REGEXP_LIKE(LOWER({column}), '{value}')")

        if not self.opt('brancos', True):
            where.append("v.NUMERO_CANDIDATO <> '95'")

        if not self.opt('nulos', True):
            where.append("v.NUMERO_CANDIDATO <> '96'")
            where.append("v.NUMERO_CANDIDATO <> '97'")

        if self.opt('turno'):
            where.append(f"v.NUM_TURNO = \'{self.options['turno']}\'")

        if self.opt('mun_filter'):
            where.append(f"v.COD_MUN_TSE = \'{self.options['mun_filter']}\'")

        if self.opt('only_elected', False):
            where.append(f"c.COD_SIT_TOT_TURNO IN ('1', '2', '3')")

        if len(where) > 0:
            return "WHERE " + "\n AND ".join(where)
        else:
            return ""



