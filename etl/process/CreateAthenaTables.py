from etl.process.AthenaCreateTableBuilder import AthenaLoadPartitionsBuilder, AthenaCreateTableBuilder
from web.cepesp.athena.client import AthenaDatabaseClient, AthenaQueryFailed


class CreateAthenaTables:
    int_columns = [
        'ID_CANDIDATO',
        'ID_LEGENDA',
        'QTDE_VOTOS',
        'QTD_APTOS',
        'QTD_COMPARECIMENTO',
        'QTD_ABSTENCOES',
        'QT_VOTOS_NOMINAIS',
        'QT_VOTOS_BRANCOS',
        'QT_VOTOS_NULOS',
        'QT_VOTOS_LEGENDA',
        'QT_VOTOS_ANULADOS_APU_SEP'
    ]
    aggregations = {2: 'uf', 4: 'meso', 5: 'micro', 6: 'mun', 7: 'munzona', 8: 'zona', 9: 'votsec'}

    def __init__(self, database, source_folder, bucket):
        self.bucket = bucket
        self.source_folder = source_folder
        self.database = database
        self.client = AthenaDatabaseClient(self.database, self.bucket, "results")

    def create_detalhe(self):
        # <editor-fold desc="detalhe = {...}" defaultstate="collapsed">
        detalhe = {

            # VOTACAO SECAO
            9: [
                'ANO_ELEICAO',
                'NUM_TURNO',
                'NUM_ZONA',
                'NUM_SECAO',
                'COD_MUN_TSE',
                'COD_MUN_IBGE',
                'NOME_MUNICIPIO',
                'CODIGO_MICRO',
                'NOME_MICRO',
                'CODIGO_MESO',
                'NOME_MESO',
                'UF',
                'NOME_UF',
                'CODIGO_MACRO',
                'NOME_MACRO',
                'DESCRICAO_ELEICAO',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QT_VOTOS_NOMINAIS',
                'QT_VOTOS_BRANCOS',
                'QT_VOTOS_NULOS',
                'QT_VOTOS_LEGENDA',
                'QT_VOTOS_ANULADOS_APU_SEP',
            ],

            # ZONA
            8: [
                'ANO_ELEICAO',
                'NUM_TURNO',
                'NUM_ZONA',
                'CODIGO_MICRO',
                'NOME_MICRO',
                'CODIGO_MESO',
                'NOME_MESO',
                'UF',
                'NOME_UF',
                'CODIGO_MACRO',
                'NOME_MACRO',
                'DESCRICAO_ELEICAO',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QT_VOTOS_NOMINAIS',
                'QT_VOTOS_BRANCOS',
                'QT_VOTOS_NULOS',
                'QT_VOTOS_LEGENDA',
                'QT_VOTOS_ANULADOS_APU_SEP',
            ],

            # MUNZONA
            7: [
                'ANO_ELEICAO',
                'NUM_TURNO',
                'NUM_ZONA',
                'COD_MUN_TSE',
                'COD_MUN_IBGE',
                'NOME_MUNICIPIO',
                'CODIGO_MICRO',
                'NOME_MICRO',
                'CODIGO_MESO',
                'NOME_MESO',
                'UF',
                'NOME_UF',
                'CODIGO_MACRO',
                'NOME_MACRO',
                'DESCRICAO_ELEICAO',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QT_VOTOS_NOMINAIS',
                'QT_VOTOS_BRANCOS',
                'QT_VOTOS_NULOS',
                'QT_VOTOS_LEGENDA',
                'QT_VOTOS_ANULADOS_APU_SEP',
            ],

            # MUNICIPIO
            6: [
                'ANO_ELEICAO',
                'NUM_TURNO',
                'COD_MUN_TSE',
                'COD_MUN_IBGE',
                'NOME_MUNICIPIO',
                'CODIGO_MICRO',
                'NOME_MICRO',
                'CODIGO_MESO',
                'NOME_MESO',
                'UF',
                'NOME_UF',
                'CODIGO_MACRO',
                'NOME_MACRO',
                'DESCRICAO_ELEICAO',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QT_VOTOS_NOMINAIS',
                'QT_VOTOS_BRANCOS',
                'QT_VOTOS_NULOS',
                'QT_VOTOS_LEGENDA',
                'QT_VOTOS_ANULADOS_APU_SEP',
            ],

            # MICRO
            5: [
                'ANO_ELEICAO',
                'NUM_TURNO',
                'CODIGO_MICRO',
                'NOME_MICRO',
                'CODIGO_MESO',
                'NOME_MESO',
                'UF',
                'NOME_UF',
                'CODIGO_MACRO',
                'NOME_MACRO',
                'DESCRICAO_ELEICAO',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QT_VOTOS_NOMINAIS',
                'QT_VOTOS_BRANCOS',
                'QT_VOTOS_NULOS',
                'QT_VOTOS_LEGENDA',
                'QT_VOTOS_ANULADOS_APU_SEP',
            ],

            # MESO
            4: [
                'ANO_ELEICAO',
                'NUM_TURNO',
                'CODIGO_MESO',
                'NOME_MESO',
                'UF',
                'NOME_UF',
                'CODIGO_MACRO',
                'NOME_MACRO',
                'DESCRICAO_ELEICAO',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QT_VOTOS_NOMINAIS',
                'QT_VOTOS_BRANCOS',
                'QT_VOTOS_NULOS',
                'QT_VOTOS_LEGENDA',
                'QT_VOTOS_ANULADOS_APU_SEP',
            ],

            # UF
            2: [
                'ANO_ELEICAO',
                'NUM_TURNO',
                'UF',
                'NOME_UF',
                'CODIGO_MACRO',
                'NOME_MACRO',
                'DESCRICAO_ELEICAO',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QT_VOTOS_NOMINAIS',
                'QT_VOTOS_BRANCOS',
                'QT_VOTOS_NULOS',
                'QT_VOTOS_LEGENDA',
                'QT_VOTOS_ANULADOS_APU_SEP',
            ]

        }
        # </editor-fold>
        for (aggregation, columns) in detalhe.items():
            name = self.aggregations[aggregation]
            table = f"detalhe_{name}"
            folder = f"detalhe/{name}"
            self._create_table(table, columns, folder, ['p_ano', 'p_cargo'])

    def create_candidatos(self):
        # <editor-fold desc="self._create_table('candidatos', [...])" defaultstate="collapsed">
        self._create_table('candidatos', [
            "ID_CANDIDATO",
            "DATA_GERACAO",
            "HORA_GERACAO",
            "ANO_ELEICAO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "SIGLA_UF",
            "SIGLA_UE",
            "DESCRICAO_UE",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "NOME_CANDIDATO",
            "SEQUENCIAL_CANDIDATO",
            "NUMERO_CANDIDATO",
            "CPF_CANDIDATO",
            "NOME_URNA_CANDIDATO",
            "COD_SITUACAO_CANDIDATURA",
            "DES_SITUACAO_CANDIDATURA",
            "NUMERO_PARTIDO",
            "SIGLA_PARTIDO",
            "NOME_PARTIDO",
            "CODIGO_LEGENDA",
            "SIGLA_LEGENDA",
            "COMPOSICAO_LEGENDA",
            "NOME_COLIGACAO",
            "CODIGO_OCUPACAO",
            "DESCRICAO_OCUPACAO",
            "DATA_NASCIMENTO",
            "NUM_TITULO_ELEITORAL_CANDIDATO",
            "IDADE_DATA_ELEICAO",
            "CODIGO_SEXO",
            "DESCRICAO_SEXO",
            "COD_GRAU_INSTRUCAO",
            "DESCRICAO_GRAU_INSTRUCAO",
            "CODIGO_ESTADO_CIVIL",
            "DESCRICAO_ESTADO_CIVIL",
            "CODIGO_COR_RACA",
            "DESCRICAO_COR_RACA",
            "CODIGO_NACIONALIDADE",
            "DESCRICAO_NACIONALIDADE",
            "SIGLA_UF_NASCIMENTO",
            "CODIGO_MUNICIPIO_NASCIMENTO",
            "NOME_MUNICIPIO_NASCIMENTO",
            "DESPESA_MAX_CAMPANHA",
            "COD_SIT_TOT_TURNO",
            "DESC_SIT_TOT_TURNO",
            "EMAIL_CANDIDATO"
        ], "candidatos", ['p_ano', 'p_cargo'])
        # </editor-fold>

    def create_legendas(self):
        # <editor-fold desc="self._create_table('legendas', [...])" defaultstate="collapsed">
        self._create_table("legendas", [
            "ID_LEGENDA",
            "ANO_ELEICAO",
            "CODIGO_CARGO",
            "COMPOSICAO_COLIGACAO",
            "DATA_GERACAO",
            "DESCRICAO_CARGO",
            "DESCRICAO_ELEICAO",
            "DESCRICAO_UE",
            "HORA_GERACAO",
            "NOME_COLIGACAO",
            "NOME_PARTIDO",
            "NUMERO_PARTIDO",
            "NUM_TURNO",
            "SEQUENCIA_COLIGACAO",
            "SIGLA_COLIGACAO",
            "SIGLA_PARTIDO",
            "SIGLA_UE",
            "SIGLA_UF",
            "TIPO_LEGENDA"
        ], "legendas", ['p_ano', 'p_cargo'])
        # </editor-fold>

    def create_bem_candidato(self):
        # <editor-fold desc="self._create_table('bem_candidato', [...])" defaultstate="collapsed">
        self._create_table("bem_candidato", [
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
            "ID_CANDIDATO"
        ], "bem_candidato", ['p_ano', 'p_uf'])
        # </editor-fold>

    def create_votos(self):
        # <editor-fold desc="votos = {...}" defaultstate="collapsed">
        votos = {

            # VOTACAO SECAO
            9: [
                "DATA_GERACAO",
                "HORA_GERACAO",
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
            ],

            # ZONA
            8: [
                "DATA_GERACAO",
                "HORA_GERACAO",
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
                "QTDE_VOTOS",
                "ID_CANDIDATO",
                "ID_LEGENDA"
            ],

            # MUNZONA
            7: [
                "DATA_GERACAO",
                "HORA_GERACAO",
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
                "QTDE_VOTOS",
                "ID_CANDIDATO",
                "ID_LEGENDA"
            ],

            # MUNICIPIO
            6: [
                "DATA_GERACAO",
                "HORA_GERACAO",
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
                "QTDE_VOTOS",
                "ID_CANDIDATO",
                "ID_LEGENDA"
            ],

            # MICRO
            5: [
                "DATA_GERACAO",
                "HORA_GERACAO",
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
                "QTDE_VOTOS",
                "ID_CANDIDATO",
                "ID_LEGENDA"
            ],

            # MESO
            4: [
                "DATA_GERACAO",
                "HORA_GERACAO",
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
                "QTDE_VOTOS",
                "ID_CANDIDATO",
                "ID_LEGENDA"
            ],

            # UF
            2: [
                "DATA_GERACAO",
                "HORA_GERACAO",
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
                "QTDE_VOTOS",
                "ID_CANDIDATO",
                "ID_LEGENDA"
            ],

        }
        # </editor-fold>
        for (aggregation, columns) in votos.items():
            name = self.aggregations[aggregation]
            table = f"votos_{name}"
            folder = f"votos/{name}"
            self._create_table(table, columns + ['ID_CANDIDATO', 'ID_LEGENDA'], folder, ['p_ano', 'p_cargo', 'p_uf'])

    def create_filiados(self):
        # <editor-fold desc="self._create_table('filiados', [...])" defaultstate="collapsed">
        self._create_table("filiados", [
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
        ], "filiados", ['p_partido', 'p_uf'])
        # </editor-fold>

    def create_secretarios(self):
        # <editor-fold desc="self._create_table('secretarios', [...])" defaultstate="collapsed">
        self._create_table('secretarios', [
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
        ], 'secretarios')
        # </editor-fold>

    def _get_column_type(self, col):
        return 'bigint' if col in self.int_columns else 'string'

    def _create_table(self, table, columns_list, folder, partitions_list=None):
        print(f"Dropping table {table}...")
        self.client.execute(f"DROP TABLE {table}", wait=True)

        print(f'Creating table {table}...')

        columns = {}
        for col in columns_list:
            columns[col] = self._get_column_type(col)

        partitions = {}
        if partitions_list is not None:
            for col in partitions_list:
                partitions[col] = self._get_column_type(col)

        builder = AthenaCreateTableBuilder()
        builder.table = table
        builder.partitions = partitions
        builder.columns = columns
        builder.location = f"s3://{self.bucket}/{self.source_folder}/{folder}"

        query = builder.build()
        try:
            self.client.execute(query, wait=True, min_wait=8)
        except AthenaQueryFailed as e:
            print(e)


class LoadAthenaPartitions:
    uf_list = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI',
               'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO', 'BR', 'VT', 'ZZ']
    parties = ["avante", "dc", "dem", "mdb", "novo", "patri", "pc_do_b", "pcb", "pco", "pdt", "phs", "pmb", "pmn",
               "pode", "pp", "ppl", "pps", "pr", "prb", "pros", "prp", "prtb", "psb", "psc", "psd", "psdb", "psl",
               "psol", "pstu", "pt", "ptb", "ptc", "pv", "rede", "solidariedade"]

    def __init__(self, database, source_folder, bucket, years, jobs):
        self.years = years
        self.jobs = jobs
        self.bucket = bucket
        self.source_folder = source_folder
        self.database = database
        self.client = AthenaDatabaseClient(self.database, self.bucket, "results")

    def load_candidatos(self):
        self._load_dim_partitions("candidatos")

    def load_legendas(self):
        self._load_dim_partitions("legendas")

    def load_votos(self):
        tables = ["votos_votsec", "votos_munzona", "votos_zona", "votos_mun", "votos_micro", "votos_meso", "votos_uf"]
        for table in tables:
            jobs = list(set(self.jobs) - {2, 4, 9, 10})

            for job in jobs:
                for year in self.years:
                    if job in [11, 13] and year in [2018, 2014, 2010, 2006, 2002, 1998]:
                        continue

                    partitions = []
                    for uf in self.uf_list:
                        if job == 1 and year in [2018, 2014, 2002] and uf != 'BR':
                            continue

                        if job == 8 and uf != 'DF':
                            continue

                        partitions.append({'p_ano': year, 'p_cargo': job, 'p_uf': uf})

                    self._load_partition(table, table.replace('_', '/'), partitions)

    def load_detalhe(self):
        tables = ["detalhe_votsec", "detalhe_munzona", "detalhe_zona", "detalhe_mun", "detalhe_micro", "detalhe_meso",
                  "detalhe_uf"]
        for table in tables:
            jobs = list(set(self.jobs) - {2, 4, 9, 10})

            for job in jobs:
                partitions = []

                for year in self.years:
                    if job in [11, 13] and year in [2018, 2014, 2010, 2006, 2002, 1998]:
                        continue

                    partitions.append({'p_ano': year, 'p_cargo': job})

                    self._load_partition(table, table.replace('_', '/'), partitions)

    def load_filiados(self):
        for party in self.parties:
            partitions = []

            for uf in self.uf_list:
                partitions.append({'p_partido': party, 'p_uf': uf})

            self._load_partition("filiados", "filiados", partitions)

    def load_bem_candidato(self):
        for year in self.years:
            partitions = []
            for uf in self.uf_list:
                partitions.append({'p_ano': year, 'p_uf': uf})

            self._load_partition("bem_candidato", "bem_candidato", partitions)

    def _load_dim_partitions(self, table):
        for year in self.years:
            partitions = []
            for job in self.jobs:
                if job in [11, 13] and year in [2018, 2014, 2010, 2006, 2002, 1998]:
                    continue

                partitions.append({'p_ano': year, 'p_cargo': job})

            self._load_partition(table, table, partitions)

    def _load_partition(self, table, folder, partitions):
        if len(partitions) == 0:
            return

        print(f"Loading partitions from {table}")

        builder = AthenaLoadPartitionsBuilder()
        builder.location = f"s3://{self.bucket}/{self.source_folder}/{folder}"
        builder.table = table
        for partition in partitions:
            builder.add_partition(partition)

        query = builder.build()
        print(query)
        try:
            self.client.execute(query, wait=True)
        except AthenaQueryFailed as e:
            print(e)
