class SecretariesColumnsSelector:

    def columns(self):
        return [
            "STATUS",
            "NOME_SECRETARIO",
            "RG",
            "SEXO",
            "NOME_MUNICIPIO_NASCIMENTO",
            "UF_NASCIMENTO",
            "CARGO",
            "ORGAO_OCUPADO",
            "UF_ORGAO_OCUPADO",
            "COD_GRAU_INSTRUCAO",
            "DESCRICAO_GRAU_INSTRUCAO",
            "CURSO_MESTRADO",
            "CURSO_DOUTORADO",
            "JA_ERA_FUNCIONARIO_PUBLICO",
            "NIVEL_DE_GOVERNO",
            "TRABALHAVA_NA_SECRETARIA_NO_MOMENTO_DA_NOMEACAO",
            "ORGAO_EM_QUE_TRABALHAVA",
            "ANO_INGRESSO_ORGAO",
            "MES_INGRESSO_ORGAO",
            "PROFISSAO_ANTES_DE_NOMEADO",
            "UF",
            "ID_SECRETARIO",
            "CPF",
            "TITULO_DE_ELEITOR",
            "ORGAO_NOME",
            "ID_CARGO",
            "ID_ORGAO",
            "DATA_ASSUMIU",
            "DATA_DEIXOU",
            "MOTIVO_SAIDA",
            "ORIGEM_FILIACAO",
            "SIGLA_PARTIDO",
            "NOME_PARTIDO",
            "CODIGO_MUNICIPIO",
            "NOME_MUNICIPIO",
            "RACA_RAIS",
            "DATA_NASCIMENTO"
        ]

    def visible_columns(self):
        return [
            "NOME_SECRETARIO",
            "RG",
            "CARGO",
            "ORGAO_OCUPADO",
            "UF_ORGAO_OCUPADO",
            "UF",
            "CPF",
            "TITULO_DE_ELEITOR",
            "DATA_ASSUMIU",
            "DATA_DEIXOU",
            "DATA_NASCIMENTO",
        ]

    def order_by_columns(self):
        return ['NOME_SECRETARIO']
