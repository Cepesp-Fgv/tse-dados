import os

import pandas as pd

from web.cepesp.votos.options import VotosMunOptions

path_base = os.path.dirname(__file__)


def read_vot_sec_2t_2012():
    file_path = os.path.join(path_base, '../../storage/votos/votsec/2012/vsec_2t_2012.csv.gz')
    return pd.read_csv(file_path, sep=',', dtype=str)


class NewVotosReader:

    def __init__(self, options: VotosMunOptions):
        self.options = options
        self.uf_list = {'BR', 'ZZ', 'VT', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
                        'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'}

        if 'UF' in self.options.filters:
            if self.options.job == 1:
                self.uf_list = {'BR', 'ZZ', 'VT', self.options.filters['UF']}
            else:
                self.uf_list = {'ZZ', 'VT', self.options.filters['UF']}

    def read(self) -> pd.DataFrame:
        df = None
        for y in self.options.years:
            year_df = self._read_year(y)
            df = df.append(year_df, ignore_index=True) if df is not None else year_df

        return df

    def _read_year(self, year: int):
        df = self._read_job(year, self.options.job)
        if self.options.job == 7:
            df = df.append(self._read_job(year, 8), ignore_index=True)

        return df

    def _read_job(self, year: int, job: int):
        df = None
        for uf in self.uf_list:
            uf_df = self._read_uf(year, job, uf)
            df = df.append(uf_df, ignore_index=True) if df is not None else uf_df

        df = self._filter_suplementar(year, job, df)

        return df

    def _read_uf(self, year: int, job: int, uf: str):
        if job in [11, 13] or self.options.reg in [7, 8]:
            regional = 'munzona'
        elif self.options.reg == 6:
            regional = 'mun'
        elif self.options.reg == 9:
            regional = 'votsec'
        else:
            regional = 'micro'

        file_name = 'votacao_secao_%d_%s.gz' % (year, uf)
        file_path = os.path.join(path_base, '../../storage/votos/%s/%d/%d/%s' % (regional, year, job, file_name))

        if os.path.exists(file_path):
            return pd.read_csv(file_path, sep=';', dtype=str, low_memory=False)
        else:
            return None

    def _filter_suplementar(self, year, job, df):
        if year == 2014 and job == 3:
            return df[~df['DESCRICAO_ELEICAO'].str.contains("Suplementar", case=False, na=False)]
        else:
            return df


class VotosMunReader:
    data_geracao_filter = {
        2010: "23/03/2012",
        2006: "16/02/2016"
    }

    def __init__(self, options: VotosMunOptions):
        self.options = options

    def read(self):
        df = None
        for y in self.options.years:
            year_df = self._read_year(y)
            df = df.append(year_df, ignore_index=True) if df is not None else year_df

        return df

    def _read_year(self, year):
        df = self._read_job(self.options.job, year)
        if self.options.job == 7:
            df = df.append(self._read_job(8, year))

        return df

    def _read_job(self, job, year):
        if self.options.reg == 9:
            df = self._read_vot_sec(job, year, self.options.uf_filter)

            if not (year in self.data_geracao_filter.keys()):
                df = df.append(self._read_vot_sec(job, year, 'BR'))

            df = df.append(self._read_vot_sec(job, year, 'VT'))
            df = df.append(self._read_vot_sec(job, year, 'ZZ'))
            if year == 2012:
                df = df.append(read_vot_sec_2t_2012())

            return df
        else:
            df = pd.read_csv(self.file_path(job, year), sep=';', low_memory=False, error_bad_lines=False,
                             index_col=False, dtype=str)
            if job == 1:
                df['SIGLA_UE'] = 'BR'
            elif job in [3, 5, 6, 7, 8]:
                df['SIGLA_UE'] = df.UF
            else:
                df['SIGLA_UE'] = df.COD_MUN_TSE

            if job == 1 and year in self.data_geracao_filter.keys():
                df = df[df.DATA_GERACAO == self.data_geracao_filter[year]]

            df = self._filter_suplementar(year, job, df)

            return df

    def file_path(self, job, year, name='000000_0.gz'):
        if job in [11, 13] or self.options.reg in [7, 8]:
            folder = 'munzona'
        elif self.options.reg == 6:
            folder = 'mun'
        else:
            folder = 'micro'

        return os.path.join(path_base, '../../storage/votos/%s/%s/%s/%s' % (folder, year, job, name))

    def _filter_suplementar(self, year, job, df):
        if year == 2014 and job == 3:
            return df[~df['DESCRICAO_ELEICAO'].str.contains("Suplementar", case=False, na=False)]
        else:
            return df

    def _read_vot_sec(self, job, year, uf):
        file_path = os.path.join(path_base,
                                 '../../storage/votos/votsec/%s/votacao_secao_%s_%s.txt.gz' % (year, year, uf))
        if not os.path.exists(file_path):
            return pd.DataFrame()

        if year == 2012 and uf != 'BR' and uf != 'VT' and uf != 'ZZ':
            sep = ','
        else:
            sep = ';'
        df = pd.read_csv(file_path, sep=sep, low_memory=False, error_bad_lines=False, index_col=False, dtype=str,
                         names=["DATA_GERACAO", "HORA_GERACAO", "ANO_ELEICAO", "NUM_TURNO", "DESCRICAO_ELEICAO",
                                "SIGLA_UF", "SIGLA_UE", "COD_MUN_TSE", "NOME_MUNICIPIO", "NUM_ZONA", "NUM_SECAO",
                                "CODIGO_CARGO", "DESCRICAO_CARGO", "NUM_VOTAVEL", "QTDE_VOTOS"])

        if uf != "BR":
            df = df[df['SIGLA_UF'] == uf]

        df = df[df['CODIGO_CARGO'] == str(job)]

        df = self._filter_suplementar(year, job, df)

        df = df.rename({'SIGLA_UF': 'UF'})

        return df
