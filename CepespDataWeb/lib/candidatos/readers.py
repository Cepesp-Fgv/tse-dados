import os
from datetime import *

import pandas as pd

path_base = os.path.dirname(__file__)


class CandidatosReader:
    def __init__(self, options):
        self.options = options

    def file_path(self, year):
        return os.path.join(path_base, '../../storage/candidatos/candidato_%s.csv.gz' % year)

    def read(self):
        df = None
        for y in self.options.years:
            if df is None:
                df = self._read_year(y)
            else:
                df = df.append(self._read_year(y))

        return df

    def _read_year(self, year):
        df = pd.read_csv(self.file_path(year), sep=';', dtype=str)
        self.format_data_nascimento(df, year)
        self.add_retro_compatibility(df, year)
        return df

    @staticmethod
    def add_retro_compatibility(df, year):
        if year < 2014:
            df["CODIGO_COR_RACA"] = "-1"
            df["DESCRICAO_COR_RACA"] = "#NE#"

        if year <= 2010:
            df["EMAIL_CANDIDATO"] = "#NE#"

    def format_data_nascimento(self, df, year):
        df = df.rename({'UF': 'SIGLA_UF'})

        # format DATA_NASCIMENTO
        if 'DATA_NASCIMENTO' in self.options.selected_columns and year <= 2010:
            for i, row in df.iterrows():
                df.set_value(i, 'DATA_NASCIMENTO', self._format_data_nascimento(row['DATA_NASCIMENTO'], year))

    @staticmethod
    def _format_data_nascimento(original_date, year):
        try:
            if 2010 >= year >= 2008:
                original_date = original_date[:-2] + "19" + original_date[-2:]
                fdate = datetime.strptime(str(original_date), '%d-%b-%Y')
                return fdate.strftime('%d/%m/%Y')
            elif year <= 2004:
                fdate = datetime.strptime(original_date, '%d%m%Y')
                return fdate.strftime('%d/%m/%Y')
            else:
                return original_date
        except:
            return original_date
