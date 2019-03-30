from web.cepesp.columns.candidatos import CandidatosColumnsSelector
from web.cepesp.columns.bem_candidato import BemCandidatoColumnsSelector
from web.cepesp.columns.legendas import LegendasColumnsSelector
from web.cepesp.columns.tse import TSEVotosColumnsSelector
from web.cepesp.columns.votos import VotosMunColumnsSelector
from web.cepesp.utils.data import guess_match_type
from web.cepesp.utils.builder import Builder


class AthenaBuilder(Builder):
    int_columns = ['ID_CANDIDATO', 'ID_LEGENDA', 'v.ID_CANDIDATO', 'v.ID_LEGENDA']

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = None

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
                value = self.escape(value)

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
        table = self.arg('table')
        pol = self.opt('pol', 0)

        if table == 'tse' and pol != 4:
            builder = TSEQueryBuilder(**self.options)
        elif table == 'tse' and pol == 4:
            builder = TSEDetalheQueryBuilder(**self.options)
        elif table == 'votos':
            builder = VotosQueryBuilder(**self.options)
        elif table == 'bem_candidato':
            builder = BemCandidatoQueryBuilder(**self.options)
        elif table in ['candidatos', 'legendas']:
            builder = DimQueryBuilder(**self.options)
        else:
            raise KeyError(f'Invalid table {table} supplied')

        return self.trim(builder.build())


class TSEDetalheQueryBuilder(AthenaBuilder):
    mun_columns = ["SIGLA_UF", "COD_MUN_IBGE", "NOME_UF", "CODIGO_MESO", "NOME_MESO",
                   "CODIGO_MICRO", "NOME_MICRO", "NOME_MUNICIPIO", "CODIGO_MACRO", "NOME_MACRO"]

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = TSEVotosColumnsSelector(4, self.arg('reg'))

    def build(self):
        table = self.table_name('detalhe')
        years = "', '".join(map(str, self.arg('years')))

        columns = set(self.selected_columns()) - set(self.selector.sum_columns())
        columns_renamed = ", ".join([f"{self._map_column(c)} AS {c}" for c in columns])
        sum_columns = ", ".join([f"SUM({self._map_column(c)}) AS {c}" for c in self.selector.sum_columns()])
        group_columns = ", ".join(map(str, range(1, len(columns) + 1)))

        return f'''
            SELECT {columns_renamed}, {sum_columns} 
            FROM {table}
            WHERE p_ano IN (\'{years}\') 
            AND {self._build_filter_job()}
            {self._build_filter_uf()}
            GROUP BY {group_columns}
            {self._build_filters('HAVING')}
            {self._build_order_by()}
        '''

    def _detalhe_table(self):
        reg = self.arg('reg')
        if reg == 9:
            return "detalhe_votsec"
        elif reg == 8:
            return "detalhe_zona"
        elif reg == 7:
            return "detalhe_munzona"
        elif reg == 6:
            return "detalhe_mun"
        elif reg == 5:
            return "votos_micro"
        elif reg == 4:
            return "votos_meso"
        else:
            return "votos_uf"

    def _build_filter_uf(self):
        uf = self.opt('uf_filter')
        if self.arg('reg') >= 2 and uf:
            return f"AND UF = '{uf}'"
        else:
            return ""

    # region def _build_filters(self, start): [...]
    def _build_filters(self, start):
        where = self._build_base_filters()

        if self.opt('mun_filter'):
            where.append(f"COD_MUN_TSE = '{self.options['mun_filter']}'")

        if self.opt('turno'):
            where.append(f"NUM_TURNO = '{self.options['turno']}'")

        if len(where) > 0:
            return f"{start} " + "\n AND ".join(where)
        else:
            return ""
    # endregion


class VotosQueryBuilder(AthenaBuilder):

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = VotosMunColumnsSelector(self.arg('reg'))

    def build(self):
        table = self.table_name("votos")
        years = "', '".join(map(str, self.arg('years')))
        columns = set(self.selected_columns()) - set(self.selector.sum_columns())
        columns_renamed = ", ".join([f"{c} AS {c}" for c in columns])
        sum_columns = ", ".join([f"SUM({c}) AS {c}" for c in self.selector.sum_columns()])
        group_columns = ", ".join(map(str, range(1, len(columns) + 1)))

        return f'''
            SELECT {columns_renamed}, {sum_columns} 
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


class BemCandidatoQueryBuilder(AthenaBuilder):

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = BemCandidatoColumnsSelector()

    def build(self):
        years = "', '".join(map(str, self.arg('years')))
        columns_renamed = ", ".join([f"{c} AS {c}" for c in self.selected_columns()])

        return f'''
            SELECT {columns_renamed}
            FROM bem_candidato
            WHERE p_ano IN (\'{years}\') 
            {self._build_filter_uf()}
            {self._build_filters('AND')}
            {self._build_order_by()}
        '''

    def _build_filter_uf(self):
        uf = self.opt('uf_filter')
        if uf:
            return f"AND SIGLA_UF = '{uf}'"
        else:
            return ""

    # region def _build_filters(self, start): [...]
    def _build_filters(self, start):
        where = self._build_base_filters()

        where.append("DESCRICAO_ELEICAO <> '2'")

        if self.opt('mun_filter'):
            where.append(f"COD_MUN_TSE = '{self.options['mun_filter']}'")

        if self.opt('turno'):
            where.append(f"NUM_TURNO = '{self.options['turno']}'")

        if len(where) > 0:
            return f"{start} " + "\n AND ".join(where)
        else:
            return ""
    # endregion


class DimQueryBuilder(AthenaBuilder):

    def __init__(self, **options):
        super().__init__(**options)
        table = self.arg('table')

        if table == 'candidatos':
            self.selector = CandidatosColumnsSelector()
        elif table == 'legendas':
            self.selector = LegendasColumnsSelector()

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


class TSEQueryBuilder(AthenaBuilder):
    # region Columns
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
        'SEQUENCIAL_CANDIDATO',
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

    # endregion

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = TSEVotosColumnsSelector(self.arg('pol'), self.arg('reg'))

    def build(self):
        pol = self.arg('pol')
        inner_query = self._build_inner_query()

        columns = ", ".join(self._get_outer_query_columns())
        candidates_join = 'LEFT JOIN candidatos as c ' \
                          'ON v.ID_CANDIDATO = c.ID_CANDIDATO ' \
                          'AND v.ANO_ELEICAO = c.ANO_ELEICAO' if pol == 2 else ''

        return f'''
            SELECT {columns}
            FROM ({inner_query}) as v
            {candidates_join}
            LEFT JOIN legendas as l ON v.ID_LEGENDA = l.ID_LEGENDA AND v.ANO_ELEICAO = l.ANO_ELEICAO
            {self._build_where()}
            {self._build_order_by()}
        '''

    def _build_inner_query(self):
        reg = self.arg('reg')
        years = "', '".join(map(str, self.arg('years')))

        columns = ", ".join(set(self.votos[reg] + ['ID_CANDIDATO']) - {'QTDE_VOTOS'})
        group_columns = ", ".join(map(str, range(1, len(self.votos[reg]) + 1)))

        return f'''
            SELECT {columns},
                SUBSTRING(NUMERO_CANDIDATO, 1, 2) AS NUMERO_PARTIDO,
                MAX(ID_LEGENDA) AS ID_LEGENDA,
                SUM(QTDE_VOTOS) AS QTDE_VOTOS
            FROM {self.table_name('votos')}
            WHERE {self._build_filter_job()}
            AND p_ano IN (\'{years}\')
            {self._build_filter_uf()}
            GROUP BY {group_columns}
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

    def _get_outer_query_columns(self):
        pol = self.arg('pol')

        def nome_candidato_replace(c):
            if c == "c.NOME_CANDIDATO AS NOME_CANDIDATO":
                nulo = "IF(v.NUMERO_PARTIDO = '96', 'VOTO NULO', c.NOME_CANDIDATO)"
                return f"IF(v.NUMERO_PARTIDO = '95', 'VOTO BRANCO', {nulo}) AS NOME_CANDIDATO"
            if c == "l.NOME_PARTIDO AS NOME_PARTIDO":
                nulo = "IF(v.NUMERO_PARTIDO = '96', 'VOTO NULO', l.NOME_PARTIDO)"
                return f"IF(v.NUMERO_PARTIDO = '95', 'VOTO BRANCO', {nulo}) AS NOME_PARTIDO"
            if c == "l.SIGLA_PARTIDO AS SIGLA_PARTIDO":
                nulo = "IF(v.NUMERO_PARTIDO = '96', 'VOTO NULO', l.SIGLA_PARTIDO)"
                return f"IF(v.NUMERO_PARTIDO = '95', 'VOTO BRANCO', {nulo}) AS SIGLA_PARTIDO"
            if c == "l.NUMERO_PARTIDO AS NUMERO_PARTIDO" and pol != 2:
                return "v.NUMERO_PARTIDO AS NUMERO_PARTIDO"
            else:
                return c

        columns = map(lambda c: f"{self._map_column(c)} AS {c}", self.selected_columns())
        columns = map(nome_candidato_replace, columns)

        return columns

    def _map_column(self, column):
        reg = self.arg('reg')
        pol = self.arg('pol')
        if column in (self.votos[reg] + ['ID_CANDIDATO', 'ID_LEGENDA']):
            return f"v.{column}"
        elif column in self.candidatos and pol == 2:
            return f"c.{column}"
        elif column in self.legendas:
            return f"l.{column}"
        else:
            return column

    # region def _build_where(self): [...]
    def _build_where(self):
        where = self._build_base_filters()
        pol = self.arg('pol')

        if not self.opt('brancos', True):
            where.append("v.NUMERO_PARTIDO <> '95'")

        if not self.opt('nulos', True):
            where.append("v.NUMERO_PARTIDO <> '96'")
            where.append("v.NUMERO_PARTIDO <> '97'")

        if self.opt('turno'):
            where.append(f"v.NUM_TURNO = \'{self.options['turno']}\'")

        if self.opt('mun_filter'):
            where.append(f"v.COD_MUN_TSE = \'{self.options['mun_filter']}\'")

        if self.opt('only_elected', False) and pol == 2:
            where.append(f"c.COD_SIT_TOT_TURNO IN ('1', '2', '3')")

        if len(where) > 0:
            return "WHERE " + "\n AND ".join(where)
        else:
            return ""
    # endregion
