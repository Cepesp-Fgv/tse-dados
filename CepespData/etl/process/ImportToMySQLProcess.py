import gzip
import shutil
from os import remove

import mysql.connector
import pandas as pd


class ImportToMySQLProcess:

    def __init__(self, config):
        self.config = config
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()

    def handle(self, item):
        self._import(item)

    def _import(self, item):
        if item['table'].startswith('votos') and item['aggregation'] != 'votsec':
            columns = self._get_columns(item)
            extracted_path = self._extract(item)
            query = self._build_query(extracted_path, item['table'], columns)
            print(query)
            self.cursor.execute(query)
            self.connection.commit()
            remove(extracted_path)

    def _get_columns(self, item):
        return pd.read_csv(item['path'], dtype=str, sep=';', nrows=1).columns.tolist()

    def _extract(self, item):
        extracted_path = item['path'].replace('.gz', '.csv')
        with open(extracted_path, 'wb+') as f_out:
            with gzip.open(item['path'], 'rb') as f_in:
                shutil.copyfileobj(f_in, f_out)

        return extracted_path

    def _build_query(self, path, table, columns):
        columns = ", ".join(columns)

        query = "LOAD DATA LOCAL INFILE '{file}' "
        query += "INTO TABLE {table} "
        query += "CHARACTER SET UTF8 "
        query += "FIELDS TERMINATED BY ';' "
        query += "OPTIONALLY ENCLOSED BY '\"' "
        query += "LINES TERMINATED BY '\\r\\n' "
        query += "IGNORE 1 LINES "
        query += "({columns})"

        file_path = path.replace('\\', '\\\\')
        return query.format(file=file_path, table=table, columns=columns)
