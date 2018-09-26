class AthenaQueryBuilder:
    votos = {

        # BR
        0: [
            "ANO_ELEICAO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
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
            "SIGLA_UE",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
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
            "SIGLA_UE",
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
            "SIGLA_UE",
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
            "SIGLA_UE",
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
            "SIGLA_UE",
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
            "SIGLA_UE",
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
            "SIGLA_UE",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NUMERO_CANDIDATO",
            "QTDE_VOTOS"
        ]

    }

    candidatos = [
        'NUMERO_PARTIDO',
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
        "SIGLA_COLIGACAO",
        "NOME_COLIGACAO",
        "COMPOSICAO_COLIGACAO",
        "SEQUENCIA_COLIGACAO"
    ]

    def __init__(self, **options):
        self.options = options

    def opt(self, key, default=None):
        return self.options[key] if key in self.options else default

    @property
    def votes_table(self):
        if self.options['reg'] == 9:
            return "votos_votsec"
        elif self.options['reg'] == 8:
            return "votos_zona"
        elif self.options['reg'] == 7:
            return "votos_munzona"
        elif self.options['reg'] == 6:
            return "votos_mun"
        elif self.options['reg'] == 5:
            return "votos_micro"
        elif self.options['reg'] == 4:
            return "votos_meso"
        else:
            return "votos_meso"

    def columns(self):
        reg = self.options['reg']
        return self.votos[reg] + self.candidatos + self.legendas

    def build(self):
        reg = self.options['reg']
        job = self.options['job']
        columns = ", ".join(set(self.votos[reg] + ['ID_CANDIDATO', 'ID_LEGENDA']) - {'QTDE_VOTOS'})
        years = "', '".join(map(str, self.options['years']))
        inner_query = f'''
            SELECT {columns}, SUM(QTDE_VOTOS) AS QTDE_VOTOS
            FROM {self.votes_table}
            WHERE CODIGO_CARGO = \'{job}\'
            AND ANO_ELEICAO IN (\'{years}\')
            GROUP BY {columns}
        '''

        columns = map(lambda c: self.map_column(c), self.columns())
        columns = ", ".join(columns)
        outer_query = f'''
            SELECT {columns}
            FROM ({inner_query}) as v
            LEFT JOIN candidatos as c ON v.ID_CANDIDATO = c.ID_CANDIDATO
            LEFT JOIN legendas as l ON v.ID_LEGENDA = l.ID_LEGENDA
            {self._build_where()}
        '''

        return outer_query.strip(" \n\t")

    def map_column(self, column):
        reg = self.options['reg']
        if column in self.votos[reg]:
            return "v.%s" % column
        elif column in self.candidatos:
            return "c.%s" % column
        elif column in self.legendas:
            return "l.%s" % column
        else:
            return column

    def _build_where(self):
        filters = self.opt('filters', {})
        where = [(column, '=', value) for column, value in filters.items()]

        if not self.opt('brancos', True):
            where.append(('NUMERO_CANDIDATO', '<>', '95'))

        if not self.opt('nulos', True):
            where.append(('NUMERO_CANDIDATO', '<>', '96'))

        if self.opt('turno'):
            where.append(('NUM_TURNO', '=', self.options['turno']))

        if self.opt('uf_filter'):
            where.append(('UF', '=', self.options['uf_filter']))

        if self.opt('mun_filter'):
            return "WHERE " + " AND ".join([f"{self.map_column(c)} {o} '{v}'" for c, o, v in where])
        else:
            return ""
