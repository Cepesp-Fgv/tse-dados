from web.cepesp.athena.builders import AthenaBuilder
from web.cepesp.athena.cache import DatabaseCacheHandler, LocalCacheHandler
from web.cepesp.athena.client import AthenaDatabaseClient
from web.cepesp.config import APP_ENV, ATHENA_CACHE
from web.cepesp.utils.data import apply_translations


class QueryNotFoundException(Exception):
    def __init__(self, query_id):
        super().__init__(f"Query not found. ({query_id})")


class AthenaQuery:

    def __init__(self):
        self.client = AthenaDatabaseClient(f"cepesp_{APP_ENV}", "cepesp-athena", "results")

        if ATHENA_CACHE == 'database':
            self.cache = DatabaseCacheHandler()
        elif ATHENA_CACHE == 'local':
            self.cache = LocalCacheHandler()
        else:
            self.cache = None

    def build_query(self, options):
        return AthenaBuilder(**options).build()

    def get_info(self, options, wait=False):
        query_id = options['query_id'] if 'query_id' in options else None
        if query_id:
            info = self.cache.get(query_id)
        else:
            query = self.build_query(options)
            info = self.cache.get_from_query(query)

            if info is None:
                query_id = self.client.execute(query, wait, min_wait=16)
                info = self.cache.save(query, query_id, options['name'])
            else:
                print('[CACHED]', info['id'], query)

        if info is None:
            raise QueryNotFoundException(query_id)

        return info

    def _get_athena_id(self, options, wait=False):
        info = self.get_info(options, wait)
        return info['athena_id']

    def get_df(self, options, wait=False):
        athena_id = self._get_athena_id(options, wait)
        df = self.client.read(athena_id, options['length'], options['start'])
        df = apply_translations(df, df.columns.tolist())

        return df

    def get_stream(self, options, wait=False):
        athena_id = self._get_athena_id(options, wait)

        return self.client.get_stream(athena_id)

    def get_status(self, options, wait=False):
        athena_id = self._get_athena_id(options, wait)
        status, reason = self.client.status(athena_id)

        if status == "FAILED":
            info = self.get_info(options, wait)
            self.cache.remove(info['id'])

        return {'status': status, 'message': reason}
