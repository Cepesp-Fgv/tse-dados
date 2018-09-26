import os

import pandas as pd

from web.cepesp.legendas.options import LegendasOptions

path_base = os.path.dirname(__file__)


class LegendasReader:
    def __init__(self, options: LegendasOptions):
        self.options = options

    def file_name(self, year):
        if self.options.job is 1:
            return 'legendas_%s_presidente.csv.gz' % year
        else:
            return 'legendas_%s.csv.gz' % year

    def file_path(self, year):
        return os.path.join(path_base, '../../storage/legendas/%s/%s' % (year, self.file_name(year)))

    def _read_year(self, year):
        df = pd.read_csv(self.file_path(year), sep=';', dtype=str)
        df = df.rename(columns={
            "SEQUENCIA_COLIGACAO": "SEQUENCIAL_COLIGACAO"
        })

        return df

    def read(self):
        df = None
        for y in self.options.years:
            if df is None:
                df = self._read_year(y)
            else:
                df = df.append(self._read_year(y))

        return df


class NewLegendasReader:

    def __init__(self, options: LegendasOptions):
        self.options = options
        self.base = os.path.join(path_base, '../../storage/legendas/')

    def read(self) -> pd.DataFrame:
        df = None
        for year in self.options.years:
            year_df = self._read_year_job(year, self.options.job)
            df = df.append(year_df, ignore_index=True) if df is not None else year_df

            if self.options.job == 7:
                year_df = self._read_year_job(year, 8)
                df = df.append(year_df, ignore_index=True)

        return df

    def _read_year_job(self, year, job) -> pd.DataFrame:
        file_name = '{y}/{j}/legendas_{y}.gz'.format(y=year, j=job)
        file_path = os.path.join(self.base, file_name)
        df = pd.read_csv(file_path, sep=';', dtype=str, low_memory=False)

        df = df.rename(columns={
            "SEQUENCIA_COLIGACAO": "SEQUENCIAL_COLIGACAO"
        })

        return df
