import hashlib
import json
import os
from datetime import datetime

from web.cepesp.config import APP_ENV
from web.cepesp.database import CacheEntry, database_client


class DatabaseCacheHandler:

    def open(self):
        try:
            database_client.connect(reuse_if_open=True)
        except:
            pass

    def close(self):
        try:
            database_client.close()
        except:
            pass

    def get(self, query_id):
        if query_id is None:
            return None

        try:
            self.open()
            entry = CacheEntry.get(CacheEntry.id == query_id)
            self.close()
            return self._output(entry)
        except:
            return None

    def get_from_query(self, query):
        if query is None:
            return None

        try:
            self.open()
            entry = CacheEntry.get(CacheEntry.sql == query)
            self.close()
            return self._output(entry)
        except:
            return None

    def save(self, query, athena_id, query_name=None):
        self.open()
        entry, exists = CacheEntry.get_or_create(
            sql=query,
            athena_id=athena_id,
            name=query_name,
            env=APP_ENV,
            created_at=datetime.now()
        )
        self.close()
        return self._output(entry)

    def remove(self, qid):
        try:
            self.open()
            q = CacheEntry.delete().where(CacheEntry.id == qid)
            q.execute()
            self.close()
        except:
            pass

    def _output(self, entry):
        return {'id': entry.id, 'athena_id': entry.athena_id, 'sql': entry.sql, 'name': entry.name}


class LocalCacheHandler:

    def __init__(self):
        self.cache_path = os.path.join(os.path.dirname(__file__), '../../static/cache')

    def get(self, query_id):
        if query_id is None:
            return None

        data = self._read(query_id)

        if data is not None:
            return data
        else:
            return None

    def get_from_query(self, query):
        return self.get(self.hash(query))

    def hash(self, query):
        return hashlib.md5(str(query).encode('utf8')).hexdigest()

    def save(self, query, athena_id, query_name=None):
        query_id = self.hash(query)
        name = athena_id if query_name is None else query_name
        data = {
            'id': query_id,
            'athena_id': athena_id,
            'name': name,
            'sql': query,
        }

        with open(self._file_path(query_id), 'w+') as fp:
            json.dump(data, fp)

        return data

    def _file_path(self, qid):
        return os.path.join(self.cache_path, qid + ".json")

    def _read(self, qid):
        cache_file_path = self._file_path(qid)

        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as fp:
                return json.load(fp)
        else:
            return None

    def remove(self, qid):
        cache_file_path = self._file_path(qid)
        try:
            os.remove(cache_file_path)
        except OSError:
            pass
