import time

import requests
from requests import Response


def run_request(uri, options) -> Response:
    url = "http://python-app.sa-east-1.elasticbeanstalk.com/api/consulta/" + uri
    r = requests.get(url, params=options)
    return r


def assert_request(uri, **options):
    print("Asserting ", {i: options[i] for i in options if i != 'selected_columns'}, "->", end='')
    start = time.time()
    result = run_request(uri, options)
    elapsed = time.time() - start

    if result.status_code == 200 and len(result.text) >= 100:
        print(" OK [%.3f ms]" % elapsed)
    else:
        print(" ERROR [%d]" % result.status_code)


def get_years(job):
    if job is 1 or job is 3 or job is 5 or job is 6 or job is 7 or job is 8:
        return [2014, 2010, 2006, 2002, 1998]
    elif job is 11 or 13:
        return [2016, 2012, 2008, 2004, 2000]


def run():
    jobs = [1, 3, 5, 6, 7, 11, 13]

    print("CANDIDATOS ----")
    for job in jobs:
        for year in get_years(job):
            assert_request("candidatos", cargo=job, ano=year)

    print("LEGENDAS ----")
    for job in jobs:
        for year in get_years(job):
            assert_request("legendas", cargo=job, ano=year)

    reg = [0, 2, 6, 7, 8, 1, 4, 5]
    pol = [1, 2, 3, 4]
    print("TSE ----")
    for job in jobs:
        for year in get_years(job):
            for r in reg:
                for p in pol:
                    assert_request("tse", cargo=job, ano=year, agregacao_regional=r, agregacao_politica=p)

    reg = [0, 2, 6, 7, 8, 1, 4, 5, 9]
    print("VOTOS ----")
    for job in jobs:
        for year in get_years(job):
            for r in reg:
                assert_request("votos", cargo=job, ano=year, agregacao_regional=r)

if __name__ == "__main__":
    run()
