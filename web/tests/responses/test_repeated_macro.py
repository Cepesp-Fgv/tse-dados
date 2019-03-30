import pandas as pd

from web.tests.utils import get_years, get_request_url


def assert_repeated_macro(ano):
    url = get_request_url("votos", ano=ano, cargo=1, agregacao_regional=1, numero_candidato=13, turno=1)
    df = pd.read_csv(url, sep=',', lineterminator='\n', encoding='utf-8', dtype=str)
    size = len(df)
    if size == 5 or size == 6:  # 5 Macro Regiões + Exterior
        print("%d - MACRO OK" % ano)
    else:
        print("%d - MACRO REPEATED" % ano)


def test():
    for y in get_years(1):
        assert_repeated_macro(y)


if __name__ == "__main__":
    test()
