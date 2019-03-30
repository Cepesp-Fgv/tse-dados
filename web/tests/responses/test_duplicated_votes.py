import pandas as pd

from web.tests.utils import get_years, get_request_url

APTOS = {
    1998: 106_049_062,
    2000: 102_644_778,
    2002: 115_166_810,
    2004: 118_464_969,
    2006: 125_826_156,
    2008: 128_746_974,
    2010: 135_721_843,
    2012: 138_544_294,
    2014: 142_821_358,
    2016: 144_048_995
}


def assert_duplicated_votes(uri, **options):
    url = get_request_url(uri, **options)
    df = pd.read_csv(url, sep=',', lineterminator='\n', encoding='utf-8', dtype=str)
    s = pd.to_numeric(df["QTDE_VOTOS"], errors='coerce').sum()

    if s > APTOS[options['ano']]:
        print(options, " - SUM(QTDE_VOTOS) = %d [DUPLICATED]" % s)
    else:
        print(options, " - SUM(QTDE_VOTOS) = %d [OK]" % s)


def test():
    for y in get_years(1):
        assert_duplicated_votes("votos", ano=y, cargo=1, agregacao_regional=6, turno=1)
        assert_duplicated_votes("votos", ano=y, cargo=1, agregacao_regional=6, turno=2)
        assert_duplicated_votes("tse", ano=y, cargo=1, agregacao_regional=6, agregacao_politica=2, turno=1, brancos=1,
                                nulos=1)
        assert_duplicated_votes("tse", ano=y, cargo=1, agregacao_regional=6, agregacao_politica=2, turno=2, brancos=1,
                                nulos=1)


if __name__ == "__main__":
    test()
