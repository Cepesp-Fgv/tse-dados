from urllib.parse import urlencode

import pandas as pd
from requests import HTTPError


class TestServerClient:

    def __init__(self, base):
        self.base = base

    def _request_url(self, table, args):
        query = urlencode(self._translate(args))
        return "{base}/api/consulta/{table}?{query}".format(base=self.base, table=table, query=query)

    def _request(self, table, args):
        url = self._request_url(table, args)
        return pd.read_csv(url, sep=',', dtype=str)

    def _translate(self, args):
        options = {'ano': args['year'], 'cargo': args['job']}
        if 'regional_aggregation' in args:
            options['agregacao_regional'] = args['regional_aggregation']

        if 'political_aggregation' in args:
            options['agregacao_politica'] = args['political_aggregation']

        if 'columns' in args:
            if isinstance(args['columns'], list):
                options['c'] = ",".join(args['columns'])
            else:
                options['c'] = args['columns']

        if 'only_elected' in args:
            options['only_elected'] = args['only_elected']

        options['sep'] = ','

        return options

    def get_votes(self, **args):
        return self._request("votos", args)

    def get_candidates(self, **args):
        return self._request("candidatos", args)

    def get_coalitions(self, **args):
        return self._request("legendas", args)

    def get_elections(self, **args):
        return self._request("tse", args)


class TestProcess:

    def __init__(self, fixes):
        self.client = TestServerClient("http://localhost:5000")
        self.fixes = fixes

    def handle(self):
        for fix in self.fixes:
            name = fix.__class__.__name__
            print("TESTING: %s" % name)

            try:
                fix.test(self.client)
                print("%s [OK]" % name)
            except AssertionError as ex:
                print("[ASSERT-ERROR] %s: %s" % (name, ex))
            except HTTPError as ex:
                print("[HTTP-ERROR][%d] %s: %s" % (ex.errno, name, ex))
            except Exception as ex:
                print("[ERROR] %s: %s" % (fix, ex))
