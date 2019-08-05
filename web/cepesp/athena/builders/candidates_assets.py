from web.cepesp.athena.builders.base import AthenaBuilder
from web.cepesp.columns.bem_candidato import CandidateAssetsColumnsSelector


class CandidateAssetsQueryBuilder(AthenaBuilder):
    bens = [
        "DATA_GERACAO",
        "HORA_GERACAO",
        "ANO_ELEICAO",
        "DESCRICAO_ELEICAO",
        "SIGLA_UF",
        "SEQUENCIAL_CANDIDATO",
        "CD_TIPO_BEM_CANDIDATO",
        "DS_TIPO_BEM_CANDIDATO",
        "DETALHE_BEM",
        "VALOR_BEM",
        "DATA_ULTIMA_ATUALIZACAO",
        "HORA_ULTIMA_ATUALIZACAO",
        "ID_CANDIDATO"
    ]

    def __init__(self, **options):
        super().__init__(**options)
        self.selector = CandidateAssetsColumnsSelector()

    def build(self):
        years = "', '".join(map(str, self.arg('years')))
        columns_renamed = ", ".join([f"{self._map_column(c)} AS {c}" for c in self.selected_columns()])

        return f'''
            SELECT DISTINCT {columns_renamed}
            FROM bem_candidato as b
            LEFT JOIN candidatos as c ON b.ID_CANDIDATO = c.ID_CANDIDATO AND c.NUM_TURNO = '1'
            WHERE b.p_ano IN (\'{years}\') 
            {self._build_filters('AND')}
            {self._build_order_by()}
        '''

    def _map_column(self, column):
        if column in self.bens:
            return f"b.{column}"
        else:
            return f"c.{column}"

    # region def _build_filters(self, start): [...]
    def _build_filters(self, start):
        where = self._build_base_filters()

        where.append("b.DESCRICAO_ELEICAO <> '2'")

        if self.opt('uf_filter'):
            return f"AND b.SIGLA_UF = '{self.opt('uf_filter')}'"

        if len(where) > 0:
            return f"{start} " + "\n AND ".join(where)
        else:
            return ""
    # endregion