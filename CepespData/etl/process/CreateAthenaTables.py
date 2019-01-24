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
        'QT_VOTOS_ANULADOS_APU_SEP',
    ]
    aggregations = {2: 'uf', 4: 'meso', 5: 'micro', 6: 'mun', 7: 'munzona', 8: 'zona', 9: 'votsec'}

    def __init__(self, database, source_folder, bucket):
        self.bucket = bucket
        self.source_folder = source_folder
        self.database = database
        self.client = AthenaDatabaseClient(self.database, self.bucket, "results")

    def create(self):
        # <editor-fold desc="self.create_dim('candidatos', [...])" defaultstate="collapsed">
        self.create_dim('candidatos', [
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
        ])
        # </editor-fold>

        # <editor-fold desc="self.create_dim('legendas', [...])" defaultstate="collapsed">
        self.create_dim("legendas", [
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
        ])
        # </editor-fold>

        # <editor-fold desc="self.create_dim('tse_detalhe', [...])" defaultstate="collapsed">
        self.create_dim("tse_detalhe", [
            "IDX",
            "ANO_ELEICAO",
            "NUM_TURNO",
            "DESCRICAO_ELEICAO",
            "CODIGO_CARGO",
            "DESCRICAO_CARGO",
            "QTD_APTOS",
            "QTD_COMPARECIMENTO",
            "QTD_ABSTENCOES",
            "QT_VOTOS_NOMINAIS",
            "QT_VOTOS_BRANCOS",
            "QT_VOTOS_NULOS",
            "QT_VOTOS_LEGENDA",
            "QT_VOTOS_ANULADOS_APU_SEP",
            "CODIGO_MACRO",
            "NOME_MACRO",
            "UF",
            "NOME_UF",
            "CODIGO_MESO",
            "NOME_MESO",
            "CODIGO_MICRO",
            "NOME_MICRO",
            "COD_MUN_TSE",
            "NOME_MUNICIPIO",
            "NOME_MICRO_y",
            "NUM_ZONA"
        ])
        # </editor-fold>

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
        for (aggregation, columns) in votos.items():
            self.create_votes(aggregation, columns + ['ID_CANDIDATO', 'ID_LEGENDA'])

    def create_dim(self, table, columns_list):
        self._create_table(table, columns_list, table, ['p_ano', 'p_cargo'])

    def create_votes(self, aggregation, columns_list):
        name = self.aggregations[aggregation]
        table = f"votos_{name}"
        folder = f"votos/{name}"
        self._create_table(table, columns_list, folder, ['p_ano', 'p_cargo', 'p_uf'])

    def _get_column_type(self, col):
        return 'bigint' if col in self.int_columns else 'string'

    def _create_table(self, table, columns_list, folder, partitions_list):
        print(f"Dropping table {table}...")
        self.client.execute(f"DROP TABLE {table}", wait=True)

        print(f'Creating table {table}...')

        columns = {}
        for col in columns_list:
            columns[col] = self._get_column_type(col)

        partitions = {}
        for col in partitions_list:
            partitions[col] = self._get_column_type(col)

        builder = AthenaCreateTableBuilder()
        builder.table = table
        builder.partitions = partitions
        builder.columns = columns
        builder.location = f"s3://{self.bucket}/{self.source_folder}/{folder}"

        query = builder.build()
        try:
            self.client.execute(query, wait=True)
        except AthenaQueryFailed as e:
            print(e)


class LoadAthenaPartitions:
    uf_list = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI',
               'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO', 'BR', 'VT', 'ZZ']

    def __init__(self, database, source_folder, bucket, years, jobs):
        self.years = years
        self.jobs = jobs
        self.bucket = bucket
        self.source_folder = source_folder
        self.database = database
        self.client = AthenaDatabaseClient(self.database, self.bucket, "results")

    def create(self):
        self.load_dim_partitions("candidatos")
        self.load_dim_partitions("legendas")

        tables = ["votos_votsec", "votos_munzona", "votos_zona", "votos_mun", "votos_micro", "votos_meso", "votos_uf"]
        for table in tables:
            self.load_votes_partitions(table)

    def load_dim_partitions(self, table):
        for year in self.years:
            partitions = []
            for job in self.jobs:
                if job in [11, 13] and year in [2018, 2014, 2010, 2006, 2002, 1998]:
                    continue

                partitions.append({'p_ano': year, 'p_cargo': job})

            self._load_partition(table, table, partitions)

    def load_votes_partitions(self, table):
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

    def _load_partition(self, table, folder, partitions):
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
