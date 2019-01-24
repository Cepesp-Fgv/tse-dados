import os
from _csv import QUOTE_ALL
from glob import glob

import pandas as pd


class DimensionsProcess:

    def __init__(self, output):
        self.output = output
        self.added_brancos = False
        self.last_id = {
            2018: 10_000_000,
            2016: 9_000_000,
            2014: 8_000_000,
            2012: 7_000_000,
            2010: 6_000_000,
            2008: 5_000_000,
            2006: 4_000_000,
            2004: 3_000_000,
            2002: 2_000_000,
            2000: 1_000_000,
            1998: 1,
        }

    def get_columns(self):
        raise NotImplemented

    def get_id_column(self):
        raise NotImplemented

    def get_brancos_df(self, item, job):
        raise NotImplemented

    def check(self, item):
        raise NotImplemented

    def done(self, item):
        return os.path.exists(self._output(item))

    def handle(self, item):
        df = pd.read_csv(item['path'], sep=';', dtype=str)
        df = self._set_ids(df, item)

        self._save(df[self.get_columns()], item)

    # region Private Methods
    def output_files(self):
        return glob(os.path.join(self.output, '*.gz'))

    def _set_ids(self, df, item):
        last_id = self.last_id[item['year']]

        df.is_copy = False
        df[self.get_id_column()] = range(last_id, last_id + len(df))

        self.last_id[item['year']] += len(df)

        return df

    def _save(self, df, item):
        output_path = self._output(item)
        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        df.to_csv(output_path, compression='gzip', sep=';', encoding='utf-8', index=False, quoting=QUOTE_ALL)

    def _output(self, item):
        return os.path.join(self.output, item['name'])
    # endregion

