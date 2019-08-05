from os import path

import pandas as pd

path_base = path.join(path.dirname(__file__), '../../')


def read_mun() -> pd.DataFrame:
    file_path = path.join(path_base, 'resources/data/aux_municipio.csv.gz')
    return pd.read_csv(file_path, sep=',', encoding='utf8', header=0)


def read_aux_mun_code() -> pd.DataFrame:
    file_path = path.join(path_base, 'resources/data/aux_mun_code.csv.gz')
    return pd.read_csv(file_path, sep=',', encoding='utf8', header=0)


def get_uf_list():
    df = read_mun().groupby(['UF']).mean()
    return [index for index, row in df.iterrows()]


def get_mun_list():
    df = read_mun().sort_values(['mun_des'], ascending=[True])

    return [(int(row['TSEcod']), row['mun_des'], row['UF']) for index, row in df.iterrows()]


def get_nomes_secretarios_list():
    df = pd.read_csv(path.join(path_base, 'resources/data/nomes_secretarios.gz'), sep=';')
    df = df.sort_values(['NOME_SECRETARIO'], ascending=[True])

    return [row['NOME_SECRETARIO'] for index, row in df.iterrows()]
