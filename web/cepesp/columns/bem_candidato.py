class BemCandidatoColumnsSelector:

    def columns(self):
        return [
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "DESCRICAO_ELEICAO",
            "SIGLA_UF",
            "SQ_CANDIDATO",
            "CD_TIPO_BEM_CANDIDATO",
            "DS_TIPO_BEM_CANDIDATO",
            "DETALHE_BEM",
            "VALOR_BEM",
            "DATA_ULTIMA_ATUALIZACAO",
            "HORA_ULTIMA_ATUALIZACAO",
        ]

    def visible_columns(self):
        return [
            "ANO_ELEICAO",
            "DESCRICAO_ELEICAO",
            "SIGLA_UF",
            "SQ_CANDIDATO",
            "DS_TIPO_BEM_CANDIDATO",
            "DETALHE_BEM",
            "VALOR_BEM",
        ]

    def order_by_columns(self):
        return ['ANO_ELEICAO', 'SIGLA_UF', 'SQ_CANDIDATO']
