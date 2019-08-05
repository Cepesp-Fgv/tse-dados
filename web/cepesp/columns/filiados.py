class PartyAffiliationsColumnsSelector:

    def columns(self):
        return [
            "DATA_EXTRACAO",
            "HORA_EXTRACAO",
            "NUMERO_INSCRICAO",
            "NOME_FILIADO",
            "SIGLA_PARTIDO",
            "NOME_PARTIDO",
            "UF",
            "COD_MUN_TSE",
            "NOME_MUNICIPIO",
            "NUM_ZONA",
            "NUM_SECAO",
            "DATA_FILIACAO",
            "SITUACAO_REGISTRO",
            "TIPO_REGISTRO",
            "DATA_PROCESSAMENTO",
            "DATA_DESFILIACAO",
            "DATA_CANCELAMENTO",
            "DATA_REGULARIZACAO",
            "MOTIVO_CANCELAMENTO"
        ]

    def visible_columns(self):
        return [
            "NUMERO_INSCRICAO",
            "NOME_FILIADO",
            "SIGLA_PARTIDO",
            "NOME_PARTIDO",
            "UF",
            "COD_MUN_TSE",
            "NOME_MUNICIPIO",
            "NUM_ZONA",
            "NUM_SECAO",
            "SITUACAO_REGISTRO"
        ]

    def order_by_columns(self):
        return ['NOME_FILIADO', 'UF', 'COD_MUN_TSE']
