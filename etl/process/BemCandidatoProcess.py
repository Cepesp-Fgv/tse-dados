import os
from _csv import QUOTE_ALL

from utils.data import resolve_conflicts


class BemCandidatoProcess:
    columns = [
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
        "ID_CANDIDATO"
    ]

    def __init__(self, candidates_path, output):
        self.output = output
        self.candidates_path = candidates_path

    def check(self, item):
        return item['database'] == "bem_candidato"

    def handle(self, item):
        chunk = 0
        cand = self.get_candidates(item['year'])

        for df in pd.read_csv(item['path'], sep=';', dtype=str, chunksize=100000):
            self.join_cand(df, cand)

            df = df[self.columns]
            self._save(df, item, chunk)

    def done(self, item):
        return os.path.exists(self._output(item))

    def _output(self, item):
        return os.path.join(self.output, item['name'])

    def join_cand(self, df, cand):
        idx = ['SEQUENCIAL_CANDIDATO']
        cand = cand.drop_duplicates(idx)

        df = df.set_index(idx)
        df = df.merge(cand.set_index(idx), how='left', left_index=True, right_index=True).reset_index()
        df = resolve_conflicts(df)

        df.loc[df['ID_CANDIDATO'].isnull(), 'ID_CANDIDATO'] = '0'

        return df

    def get_candidates(self, year):
        df = None

        path = os.path.join(self.candidates_path, "candidato_%d.gz" % year)
        if os.path.exists(path):
            df = pd.read_csv(path, sep=';', dtype=str)

        path = os.path.join(self.candidates_path, "candidato_%d_presidente.gz" % year)
        if os.path.exists(path):
            pres_df = pd.read_csv(path, sep=';', dtype=str)
            df = df.append(pres_df, ignore_index=True) if df is not None else pres_df

        return df

    def _save(self, df, item, chunk):
        output_path = self._output(item)

        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        header = chunk == 0
        mode = 'a' if chunk > 0 else 'w+'
        df.to_csv(output_path, mode=mode, header=header, compression='gzip', sep=';', encoding='utf-8',
                  index=False,
                  quoting=QUOTE_ALL)

    def output_files(self):
        return glob(os.path.join(self.output, '*.gz'))
