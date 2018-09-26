import hashlib
import json
import os

from web.cepesp.athena.builder import AthenaQueryBuilder
from web.cepesp.athena.client import AthenaDatabaseClient
from web.cepesp.athena.options import AthenaQueryOptions
from web.cepesp.utils.data import apply_order_by, apply_translations


class AthenaQuery:

    def __init__(self):
        self.options = AthenaQueryOptions()
        self.client = AthenaDatabaseClient("cepesp", "cepesp-athena", "results")
        self.builder = AthenaQueryBuilder(**self.options.__dict__)
        self.cache_path = os.path.join(os.path.dirname(__file__), '../../static/cache/athena.json')

    def get(self, nrows=None, skiprows=0):
        query = self.builder.build()
        query_id = self._get_cache(query)

        if query_id is None:
            query_id = self.client.execute_and_wait(query)
            self._save_cache(query, query_id)

        df = self.client.read(query_id, nrows, skiprows)

        df = df.rename(columns={
            'EMAIL_CANDIDATO': 'NM_EMAIL'
        })

        df = df[self.options.selected_columns]
        df = apply_order_by(df, self.options.selected_columns, self.options.order_by_columns)
        df = apply_translations(df, self.options.selected_columns)

        return df

    def get_stream(self):
        query = self.builder.build()
        query_id = self._get_cache(query)

        if query_id is None:
            query_id = self.client.execute_and_wait(query)
            self._save_cache(query, query_id)

        return self.client.get_stream(query_id)

    def _get_cache(self, query):
        data = self._read_cache()
        hs = self._hash(query)

        if hs in data.keys():
            return data[hs]
        else:
            return None

    def _hash(self, query):
        return hashlib.sha1(query.encode('utf-8')).hexdigest()

    def _save_cache(self, query, query_id):
        data = self._read_cache()
        hs = self._hash(query)
        data[hs] = query_id

        with open(self.cache_path, 'w+') as fp:
            json.dump(data, fp)

    def _read_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'r') as fp:
                data = json.load(fp)
        else:
            data = {}

        return data
