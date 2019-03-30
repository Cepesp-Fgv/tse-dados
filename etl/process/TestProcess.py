import time
import traceback

import pandas as pd
import requests
from requests import HTTPError


class QueryFailedException(Exception):
    pass


class CepespClient:

    def __init__(self, base):
        self.base = base
        self.headers = {
            'Accept': 'application/json'
        }

    def _get_query_id(self, table, args):
        args['table'] = table
        url = self.base + "/api/consulta/athena/query"
        response = requests.get(url, self._translate(args), headers=self.headers).json()
        if 'error' in response:
            raise QueryFailedException(response['error'])

        return response['id']

    def _get_query_status(self, query_id):
        url = self.base + "/api/consulta/athena/status"
        response = requests.get(url, {'id': query_id}, headers=self.headers).json()
        if 'error' in response:
            raise QueryFailedException(response['error'])

        return response['status'], response['message']

    def _get_query_result(self, query_id):
        url = self.base + "/api/consulta/athena/result?id=" + query_id

        try:
            df = pd.read_csv(url, sep=',', dtype=str)
            df.columns = map(str.upper, df.columns)
        except HTTPError as e:
            raise QueryFailedException(str(e))

        return df

    def _request(self, table, args):
        query_id = self._get_query_id(table, args)
        status, message = ("RUNNING", None)
        sleep = 1

        while status in ["RUNNING", "QUEUED"]:
            status, message = self._get_query_status(query_id)
            time.sleep(sleep)
            sleep *= 2

        if status == "FAILED":
            raise QueryFailedException(message)

        return self._get_query_result(query_id)

    def _translate(self, args):
        options = {'table': args['table'], 'ano': args['year'], 'filters': []}

        if 'position' in args:
            options['cargo'] = args['position']
        elif 'job' in args:
            options['cargo'] = args['job']
        else:
            raise Exception('Position argument is mandatory')

        if 'regional_aggregation' in args:
            options['agregacao_regional'] = args['regional_aggregation']
        elif 'reg' in args:
            options['agregacao_regional'] = args['reg']

        if 'political_aggregation' in args:
            options['agregacao_politica'] = args['political_aggregation']
        elif 'pol' in args:
            options['agregacao_politica'] = args['pol']

        if 'columns' in args:
            if isinstance(args['columns'], list):
                options['c'] = ",".join(args['columns'])
            else:
                options['c'] = args['columns']

        if 'filters' in args and isinstance(args['filters'], dict):
            for column in args['filters']:
                value = args['filters'][column]
                options['filters[' + column + ']'] = value

        if 'uf' in args:
            options['uf_filter'] = args['uf']

        if 'mun' in args:
            options['mun_filter'] = args['mun']

        if 'candidate_number' in args:
            options['filters[NUMERO_CANDIDATO]'] = args['candidate_number']

        if 'party' in args:
            options['filters[NUMERO_PARTIDO]'] = args['party']

        if 'only_elected' in args:
            options['only_elected'] = args['only_elected']

        options['sep'] = ','
        options['brancos'] = 1
        options['nulos'] = 1

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
        self.client = CepespClient("http://localhost:5000")
        self.fixes = fixes

    def handle(self):
        for fix in self.fixes:
            name = fix.__class__.__name__

            if self._has_test_method(fix):
                print("TESTING: %s" % name, end='')
                try:
                    fix.test(self.client)
                    print(" [OK]")
                except AssertionError as ex:
                    print(" [ASSERT-ERROR] %s: %s" % (name, ex))
                except HTTPError as ex:
                    print(" [HTTP-ERROR][%d] %s: %s" % (ex.errno, name, ex))
                except QueryFailedException as ex:
                    print(" [QUERY-ERROR] %s: %s" % (name, ex))
                except Exception as ex:
                    print(" [ERROR] %s: %s" % (name, ex))
                    traceback.print_exc()
            else:
                print("[WARN] %s has no test method" % name)

    def _has_test_method(self, fix):
        method = getattr(fix, "test", None)
        return callable(method)
