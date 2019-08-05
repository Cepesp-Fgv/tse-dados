import os
import pandas as pd
from _csv import QUOTE_ALL


class PartitioningFiliadosProcess:
    columns = [
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

    def __init__(self, output):
        self.output = output

    def check(self, item):
        return item['database'] == 'filiados'

    def done(self, item):
        return os.path.exists(self._output(item))

    def handle(self, item):
        df = pd.read_csv(item['path'], sep=';', dtype=str)
        df.fillna('#NE#')

        if not os.path.exists(self._output(item)):
            self._save(df, item)

    def _save(self, df, item):
        output_path = self._output(item)

        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        df = df[self.columns]
        df.to_csv(output_path, header=True, compression='gzip', sep=';', encoding='utf-8', index=False,
                  quoting=QUOTE_ALL)

    def _output(self, item):
        return os.path.join(self.output, str(item['party']), item['uf'], item['name'])
