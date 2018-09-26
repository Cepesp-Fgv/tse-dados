from os import path

import pandas as pd

path_base = path.join(path.dirname(__file__), '../../')


def read_mun():
    file_path = path.join(path_base, 'storage/aux_municipio.csv.gz')
    return pd.read_csv(file_path, sep=',', encoding='utf8', header=0)


def read_aux_mun_code():
    file_path = path.join(path_base, 'storage/aux_mun_code.csv.gz')
    return pd.read_csv(file_path, sep=',', encoding='utf8', header=0)


def get_uf_list():
    df = read_mun().groupby(['UF']).mean()
    return [index for index, row in df.iterrows()]


def get_mun_list():
    df = read_mun().sort_values(['mun_des'], ascending=[True])

    return [(int(row['TSEcod']), row['mun_des'], row['UF']) for index, row in df.iterrows()]
