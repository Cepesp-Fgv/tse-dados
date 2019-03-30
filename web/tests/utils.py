from urllib.parse import urlencode

import requests
from requests import Response


def get_years(job):
    if job is 1 or job is 3 or job is 5 or job is 6 or job is 7 or job is 8:
        return [2018, 2014, 2010, 2006, 2002, 1998]
    elif job is 11 or 13:
        return [2016, 2012, 2008, 2004, 2000]


def get_request_url(uri, **options):
    url = "http://test.cepesp.io/api/consulta/" + uri
    return url + "?" + urlencode(options)


def run_request(uri, **options) -> Response:
    r = requests.get(get_request_url(uri, **options))
    return r


