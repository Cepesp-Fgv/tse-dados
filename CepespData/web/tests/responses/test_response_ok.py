import re
import time

from web.tests.utils import get_years, run_request


def assert_request(uri, **options):
    print("Asserting ", {i: options[i] for i in options if i != 'selected_columns'}, "->", end='')
    start = time.time()
    result = run_request(uri, **options)
    elapsed = time.time() - start

    if result.status_code != 200:
        print(" ERROR [%d]" % result.status_code)
    else:
        print(" OK [%.3f ms]" % elapsed, end=' ')

        if re.match(r'([^\n]*\n|[^\n]+$){3,}', result.text):
            print("")
        else:
            print("[EMPTY]")


def assert_votos(jobs):
    reg = [0, 2, 6, 7, 8, 1, 4, 5, 9]

    print("VOTOS ----")
    for job in jobs:
        for year in get_years(job):
            for r in reg:
                assert_request("votos", cargo=job, ano=year, agregacao_regional=r)


def assert_tse(jobs):
    reg = [0, 2, 6, 7, 8, 1, 4, 5, 9]
    pol = [2]

    print("TSE ----")
    for job in jobs:
        for year in get_years(job):
            if year in [2014, 2010]:
                for r in reg:
                    for p in pol:
                        assert_request("tse", cargo=job, ano=year, agregacao_regional=r, agregacao_politica=p, start=0,
                                       length=15)


def assert_legendas(jobs):
    print("LEGENDAS ----")
    for job in jobs:
        for year in get_years(job):
            assert_request("legendas", cargo=job, ano=year)


def assert_candidatos(jobs):
    print("CANDIDATOS ----")
    for job in jobs:
        for year in get_years(job):
            assert_request("candidatos", cargo=job, ano=year)


def test():
    jobs = [1, 3, 5, 6, 7, 11, 13]

    # assert_candidatos(jobs)
    # assert_legendas(jobs)
    # assert_votos(jobs)
    assert_tse(jobs)


if __name__ == "__main__":
    test()
