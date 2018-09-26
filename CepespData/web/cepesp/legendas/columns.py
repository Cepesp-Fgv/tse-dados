class LegendasColumnsSelector:
    columns_list = [
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
        "SEQUENCIAL_COLIGACAO"
    ]

    def columns(self):
        return self.columns_list

    def visible_columns(self):
        columns = ['ANO_ELEICAO', 'NUM_TURNO', 'SIGLA_UF', 'SIGLA_UE', 'CODIGO_CARGO', 'NUMERO_PARTIDO',
                   'SIGLA_PARTIDO', 'COMPOSICAO_COLIGACAO', 'TIPO_LEGENDA']
        return columns

    def order_by_columns(self):
        return ['ANO_ELEICAO', 'SIGLA_UF', 'SIGLA_UE', 'CODIGO_CARGO', 'NUMERO_PARTIDO']
