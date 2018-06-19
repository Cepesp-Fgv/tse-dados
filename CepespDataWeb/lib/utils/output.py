import gzip
import hashlib
import json
from _csv import QUOTE_ALL
from os import path
from tempfile import NamedTemporaryFile

import pandas as pd
from flask import request, make_response, send_file


class ResponseConverter:
    CSV = 'csv'
    JSON = 'json'
    GZIP = 'gzip'

    def __init__(self, name):
        self._name = name
        self.type = request.args.get('format', 'csv')
        self.draw = request.args.get("draw", 0, int)
        self.start = request.args.get("start", 0, int)
        self.length = request.args.get("length", -1, int)
        self.end = self.start + self.length

        self._ext = {
            self.CSV: '.csv',
            self.JSON: '.json',
            self.GZIP: '.gz',
        }

        self._mimetype = {
            self.CSV: 'text/csv',
            self.JSON: 'application/json',
            self.GZIP: 'application/x-gzip',
        }

    @property
    def name(self):
        return self._name + self._ext[self.type]

    @property
    def mimetype(self):
        return self._mimetype[self.type]

    def parse(self, result, total, filtered_count):

        if self.length > 0:
            result = result[self.start:self.end]

        if self.type == self.CSV:
            return self._parse_csv(result)

        elif self.type == self.GZIP:
            return self._parse_gzip(result)

        elif self.type == self.JSON:
            return '{"draw":%s,"records_total":%s,"recordsFiltered":%s,"data":%s,"error":%s}' \
                   % (self.draw, total, filtered_count, result.to_json(orient='records'), 'null')

    def convert(self, output, total, filtered):
        output = self.parse(output, total, filtered)

        if isinstance(output, str):
            response = make_response(output)
            response.headers['Content-Disposition'] = 'attachment; filename=%s' % self.name
            response.headers['Content-Length'] = str(len(output))

            response.mimetype = self.mimetype
            return response
        else:
            return send_file(
                output,
                mimetype=self.mimetype,
                attachment_filename=self.name,
                as_attachment=True
            )

    def _parse_gzip(self, result: pd.DataFrame):
        tmp = NamedTemporaryFile()
        with gzip.GzipFile(mode='w+', fileobj=tmp) as gz:
            gz.write(self._parse_csv(result).encode('utf-8'))

        tmp.flush()
        tmp.seek(0)

        return tmp

    @staticmethod
    def _parse_csv(result: pd.DataFrame) -> str:
        return result.to_csv(header=True, index=False, encoding='utf8', quoting=QUOTE_ALL)


path_base = path.join(path.dirname(__file__), '../../')


class CachedQuery:
    def __init__(self, query):
        self.query = query
        self.enabled = not (not (request.args.get('cache', 1)))
        self.hashcode = self.hash(self.query.options)
        self.cache_file_path = path.join(path_base, 'static', 'cache', self.hashcode + '.gz')

    @staticmethod
    def hash(options):
        return hashlib.sha1(json.dumps(options.__dict__).encode('utf-8')).hexdigest()

    def save_cache(self, df):
        df.to_csv(self.cache_file_path, header=True, index=False, quoting=QUOTE_ALL, compression='gzip')

    def read_cache(self):
        return pd.read_csv(self.cache_file_path, compression='gzip', low_memory=False, error_bad_lines=False,
                           index_col=False, dtype=str)

    def get(self):
        if self.enabled and path.exists(self.cache_file_path):
            df = self.read_cache()
            size = len(df)
            return [df, size, size]
        else:
            result = self.query.get()
            self.save_cache(result[0])

            return result
