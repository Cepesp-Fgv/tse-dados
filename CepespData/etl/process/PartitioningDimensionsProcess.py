import os
from _csv import QUOTE_ALL

import pandas as pd


class PartitioningDimensionsProcess:

    def __init__(self, jobs, output):
        self.output = output
        self.jobs = jobs

    def check(self, item):
        return item['table'] in ["candidatos", "legendas"]

    def done(self, item):
        for job in self._get_jobs(item):
            if not os.path.exists(self._output(item, job)):
                return False

        return True

    def handle(self, item):
        df = pd.read_csv(item['path'], sep=';', dtype=str)

        for job in self.jobs:
            job_df = df[df['CODIGO_CARGO'] == str(job)]
            if not job_df.empty:
                self._save(job_df, item, job)

    def _output(self, item, job):
        return os.path.join(self.output, str(item['year']), str(job), item['name'])

    def _save(self, df, item, job):
        output_path = self._output(item, job)

        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        df.to_csv(output_path, header=True, compression='gzip', sep=';', encoding='utf-8', index=False,
                  quoting=QUOTE_ALL)

    def _get_jobs(self, item):
        if item['year'] in [1998, 2002, 2006, 2010, 2014]:
            return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        else:
            return [11, 13]
