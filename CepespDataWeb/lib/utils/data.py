from flask_babel import gettext


def unique_list(l):
    x = []
    for a in l:
        if a not in x:
            x.append(a)
    return x


def get_years(job):
    if job is 1 or job is 3 or job is 5 or job is 6 or job is 7 or job is 8:
        return [2014, 2010, 2006, 2002, 1998]
    elif job is 11 or 13:
        return [2016, 2012, 2008, 2004, 2000]


def apply_filters(df, filters):
    for column, filter_value in filters.items():
        if column in df.columns:
            filter_type = guess_match_type(filter_value)
            if filter_type == "string":
                df = df[df[column].str.contains(filter_value, case=False, na=False)]
            elif filter_type == "int":
                df = df[df[column].astype(str) == str(filter_value)]
            elif filter_type == "list":
                df = df[df[column].isin(filter_value)]

    return df


def apply_order_by(df, selected_columns: list, order_by_columns: list):
    sort = [x for x in selected_columns if x in order_by_columns and x]
    asc = [True for s in sort]
    if len(sort) > 0:
        df.sort_values(sort, ascending=asc, inplace=True)

    return df


def apply_translations(df, selected_columns: list):
    translations = {}
    for c in selected_columns:
        translations[c] = gettext('columns.' + c)

    df.rename(columns=translations, inplace=True)
    return df


def guess_match_type(value):
    if isinstance(value, (list, tuple)):
        return "list"
    else:
        try:
            int(value)
            return "int"
        except:
            return "string"


COD_SIT = {
    1998: [2, 4],
    2000: [1, 2, 4],
    2002: [2, 4],
    2004: [2, 4],
    2006: [2, 4, 16],
    2008: [2, 4, 8, 16, 17],
    2010: [2, 4, 16, 17, 18],
    2012: [2, 4, 8, 16, 17, 18],
    2014: [2, 4, 16, 17],
    2016: [2, 4, 8, 16, 17, 18, 19],
}

JOBS = {
    1: 'PRESIDENTE',
    3: 'GOVERNADOR',
    5: 'SENADOR',
    6: 'DEPUTADO_FEDERAL',
    7: 'DEPUTADO_ESTADUAL',
    8: 'DEPUTADO_DISTRITAL',
    11: 'PREFEITO',
    13: 'VEREADOR'
}

REG = {
    0: 'BR',
    1: 'MACRO',
    2: 'UF',
    4: 'MESO',
    5: 'MICRO',
    6: 'MUNICIPIO',
    7: 'MUNZONA',
    8: 'ZONA',
    9: 'VOTACAO_SECAO'
}

POL = {
    2: 'CANDIDATO',
    1: 'PARTIDO',
    3: 'COLIGACAO',
    4: 'DETALHE'
}
