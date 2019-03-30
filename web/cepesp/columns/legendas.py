class LegendasColumnsSelector:

    def columns(self):
        return [
            "ID_LEGENDA",
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "SIGLA_UF",
            "SIGLA_UE",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "TIPO_LEGENDA",
            "NUMERO_PARTIDO",
            "SIGLA_PARTIDO",
            "NOME_PARTIDO",
            "SIGLA_COLIGACAO",
            "NOME_COLIGACAO",
            "COMPOSICAO_COLIGACAO",
            "SEQUENCIA_COLIGACAO"
        ]

    def visible_columns(self):
        return ['ANO_ELEICAO', 'NUM_TURNO', 'SIGLA_UF', 'SIGLA_UE', 'CODIGO_CARGO', 'NUMERO_PARTIDO',
                'SIGLA_PARTIDO', 'COMPOSICAO_COLIGACAO', 'TIPO_LEGENDA']

    def order_by_columns(self):
        return ['ANO_ELEICAO', 'SIGLA_UF', 'SIGLA_UE', 'CODIGO_CARGO', 'NUMERO_PARTIDO']
