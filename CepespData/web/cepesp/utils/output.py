import gzip
import hashlib
import json
from _csv import QUOTE_ALL
from io import BytesIO
from os import path
from tempfile import NamedTemporaryFile

import pandas as pd
from flask import request, send_file


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
        self.sep = request.args.get("sep", ',')
        self.end = self.start + self.length
        self.paginate_inner = True

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

        if self.type == self.CSV:
            return self._parse_csv(result)

        elif self.type == self.GZIP:
            return self._parse_gzip(result)

        elif self.type == self.JSON:
            if self.length > 0 and self.paginate_inner:
                result = result[self.start:self.end]

            return '{"draw":%s,"recordsTotal":%s,"recordsFiltered":%s,"data":%s,"error":%s}' \
                   % (self.draw, total, filtered_count, result.to_json(orient='records'), 'null')

    def convert(self, output, total=0, filtered=0):
        output = self.parse(output, total, filtered)

        if isinstance(output, str):
            output = BytesIO(output.encode('utf-8'))

        return self.convert_stream(output)

    def convert_stream(self, stream):
        return send_file(stream, mimetype=self.mimetype, attachment_filename=self.name, as_attachment=True)

    def _parse_gzip(self, result: pd.DataFrame):
        tmp = NamedTemporaryFile()
        with gzip.GzipFile(mode='w+', fileobj=tmp) as gz:
            gz.write(self._parse_csv(result).encode('utf-8'))

        tmp.flush()
        tmp.seek(0)

        return tmp

    def _parse_csv(self, result: pd.DataFrame) -> str:
        return result.to_csv(header=True, index=False, encoding='utf8', sep=self.sep, quoting=QUOTE_ALL)


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

    def save_cache(self, df: pd.DataFrame):
        if not df.empty:
            df.to_csv(self.cache_file_path, header=True, index=False, quoting=QUOTE_ALL, compression='gzip')

    def read_cache(self):
        return pd.read_csv(self.cache_file_path, compression='gzip', error_bad_lines=False, index_col=False, dtype=str)

    def get(self):
        if self.enabled and path.exists(self.cache_file_path):
            df = self.read_cache()
            size = len(df)
            return [df, size, size]
        else:
            result = self.query.get()
            self.save_cache(result[0])

            return result
