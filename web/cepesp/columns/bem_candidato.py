class CandidateAssetsColumnsSelector:

    def columns(self):
        return [
            # BEM CANDIDATO
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "DESCRICAO_ELEICAO",
            "SIGLA_UF",
            "SIGLA_UE",
            "SEQUENCIAL_CANDIDATO",
            "CD_TIPO_BEM_CANDIDATO",
            "DS_TIPO_BEM_CANDIDATO",
            "DETALHE_BEM",
            "VALOR_BEM",
            "DATA_ULTIMA_ATUALIZACAO",
            "HORA_ULTIMA_ATUALIZACAO",
            "ID_CANDIDATO",

            # CANDIDATO
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NOME_CANDIDATO",
            "NUMERO_CANDIDATO",
            "NUMERO_PARTIDO",
            "SIGLA_PARTIDO",
            "CPF_CANDIDATO",
            "NUM_TITULO_ELEITORAL_CANDIDATO",
            "COD_SIT_TOT_TURNO",
            "DESC_SIT_TOT_TURNO"
        ]

    def visible_columns(self):
        return [
            "ANO_ELEICAO",
            "SIGLA_UF",
            "SIGLA_UE",
            "DS_TIPO_BEM_CANDIDATO",
            "DETALHE_BEM",
            "VALOR_BEM",
            "DESCRICAO_CARGO",
            "NOME_CANDIDATO",
            "NUMERO_CANDIDATO",
            "SIGLA_PARTIDO",
            "CPF_CANDIDATO",
            "DESC_SIT_TOT_TURNO",
        ]

    def order_by_columns(self):
        return ['ANO_ELEICAO', 'SIGLA_UF', 'SEQUENCIAL_CANDIDATO']
