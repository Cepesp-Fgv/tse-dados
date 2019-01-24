import zlib
import json
import os


class AthenaCacheHandler:

    def __init__(self):
        self.cache_path = os.path.join(os.path.dirname(__file__), '../../static/cache')

    def get(self, query_id):
        if query_id is None:
            return None

        data = self._read(query_id)

        if data is not None:
            print('query is cached:', data['athena_id'])
            return data
        else:
            return None

    def get_from_query(self, query):
        return self.get(self.hash(query))

    def get_or_save(self, query, athena_id, query_name):
        info = self.get_from_query(query)
        if info is None:
            info = self.save(query, athena_id, query_name)

        return info

    def hash(self, query):
        return '{:x}'.format(hash(query))

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
