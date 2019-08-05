import os
import pandas as pd
from _csv import QUOTE_ALL


class PartitioningBemCandidatoProcess:
    columns = [
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
    ]

    def __init__(self, output):
        self.output = output

    def check(self, item):
        return item['database'] == 'bem_candidato'

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
        return os.path.join(self.output, str(item['year']), item['uf'], item['name'])
