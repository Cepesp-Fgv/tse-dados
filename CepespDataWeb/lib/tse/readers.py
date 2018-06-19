import os

import pandas as pd

from lib.tse.options import TSEVotosOptions

path_base = os.path.dirname(__file__)


class TSEVotosReader:
    def __init__(self, options: TSEVotosOptions):
        self.options = options

    def read(self):
        df = None
        for y in self.options.years:
            if df is None:
                df = self._read_year(y)
            else:
                df = df.append(self._read_year(y))

        return df

    def _read_year(self, year):
        df = self._read_job(self.options.job, year)
        if self.options.job == 7:
            df = df.append(self._read_job(8, year))

        return df

    def _read_job(self, job, year):
        df = self._read(self.file_path(job, year))

        if os.path.exists(self.file_path(job, year, '000001_0.gz')):
            df = df.append(self._read(self.file_path(job, year, '000001_0.gz')))

        if os.path.exists(self.legenda_path(job, year)):
            try:
                df = df.append(self._read(self.legenda_path(job, year)))
            except:
                print('rebuild legenda %d %d %d' % (self.options.reg, year, job))

        if self.options.pol != 4:
            if os.path.exists(self.brancos_path(job, year)) and self.options.brancos:
                try:
                    df = df.append(self._read(self.brancos_path(job, year)))
                except:
                    print('rebuild brancos %d %d %d' % (self.options.reg, year, job))

            if os.path.exists(self.nulos_path(job, year)) and self.options.nulos:
                try:
                    df = df.append(self._read(self.nulos_path(job, year)))
                except:
                    print('rebuild nulos %d %d %d' % (self.options.reg, year, job))

        if year == 2014 and job == 3:
            df = df[~df['DESCRICAO_ELEICAO'].str.contains("Suplementar", case=False, na=False)]

        return df

    def _read(self, file_path):
        return pd.read_csv(file_path, sep=';', dtype=str)

    def file_path(self, cargo, year, name='000000_0.gz'):
        if self.options.pol == 4:
            folder = 'detalhe'
        else:
            if self.options.reg == 7 or self.options.reg == 8:
                folder = 'munzona'
            elif self.options.reg == 6:
                folder = 'mun'
            else:
                folder = 'micro'

        return os.path.join(path_base, '../../storage/%s/%s/%s/%s' % (folder, year, cargo, name))

    def brancos_path(self, cargo, year):
        return self.file_path(cargo, year, 'brancos/000000_0.gz')

    def nulos_path(self, cargo, year):
        return self.file_path(cargo, year, 'nulos/000000_0.gz')

    def legenda_path(self, cargo, year):
        return self.file_path(cargo, year, 'legenda/000000_0.gz')
