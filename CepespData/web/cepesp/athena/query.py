from web.cepesp.athena.builders import AthenaBuilder
from web.cepesp.athena.cache import AthenaCacheHandler
from web.cepesp.athena.client import AthenaDatabaseClient
from web.cepesp.config import APP_ENV
from web.cepesp.utils.data import apply_translations


class QueryNotFoundException(Exception):
    def __init__(self, query_id):
        super().__init__(f"Query not found. ({query_id})")


class AthenaQuery:

    def __init__(self):
        self.client = AthenaDatabaseClient("cepesp_" + APP_ENV, "cepesp-athena", "results")
        self.cache = AthenaCacheHandler()

    def build_query(self, options):
        return AthenaBuilder(**options).build()

    def get_info(self, options, wait=False):
        query_id = options['query_id'] if 'query_id' in options else None
        if query_id:
            info = self.cache.get(query_id)
        else:
            query = self.build_query(options)
            query_id = self.client.execute(query, wait)
            info = self.cache.get_or_save(query, query_id, options['name'])

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

        return {'status': status, 'message': reason}
