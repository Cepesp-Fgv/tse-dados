class VotesColumnsSelector:
    columns_list = {

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

    def __init__(self, reg):
        self.reg = reg

    def columns(self):
        return self.columns_list[self.reg] + ["ID_CANDIDATO", "ID_LEGENDA"]

    def visible_columns(self):
        columns = ["ANO_ELEICAO", "NUM_TURNO", "NUMERO_CANDIDATO"]

        if self.reg == 5:
            columns += ["NOME_MICRO"]
        elif self.reg == 4:
            columns += ["UF", "NOME_MESO"]
        elif self.reg == 2:
            columns += ["UF"]
        elif self.reg == 1:
            columns += ["NOME_MACRO"]
        elif self.reg == 6:
            columns += ["UF", "COD_MUN_TSE", "NOME_MUNICIPIO"]
        elif self.reg == 7:
            columns += ["UF", "COD_MUN_TSE", "NOME_MUNICIPIO", "NUM_ZONA"]
        elif self.reg == 8:
            columns += ["UF", "NUM_ZONA"]

        columns += ["DESCRICAO_CARGO", "QTDE_VOTOS"]

        return columns

    def sum_columns(self):
        return ["QTDE_VOTOS"]

    def order_by_columns(self):
        if self.reg == 9:
            return ["ANO_ELEICAO", "UF", "CODIGO_CARGO", "NUMERO_CANDIDATO"]
        else:
            return ["UF", "NUM_ZONA", "NUM_TURNO", "COD_MUN_IBGE", "NUMERO_CANDIDATO"]
