import pandas as pd


def apply_description(df: pd.DataFrame):
    df.loc[df['COD_SIT_TOT_TURNO'].isnull(), 'COD_SIT_TOT_TURNO'] = '-1'
    df.loc[df['COD_SIT_TOT_TURNO'] == '-1', 'DESC_SIT_TOT_TURNO'] = '#NULO#'
    df.loc[df['COD_SIT_TOT_TURNO'] == '1', 'DESC_SIT_TOT_TURNO'] = 'ELEITO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'DESC_SIT_TOT_TURNO'] = 'ELEITO POR MEDIA'
    df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'DESC_SIT_TOT_TURNO'] = 'ELEITO POR QP'
    df.loc[df['COD_SIT_TOT_TURNO'] == '4', 'DESC_SIT_TOT_TURNO'] = 'NÃO ELEITO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'DESC_SIT_TOT_TURNO'] = '2º TURNO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'DESC_SIT_TOT_TURNO'] = 'SUPLENTE'
    df.loc[df['COD_SIT_TOT_TURNO'] == '9', 'DESC_SIT_TOT_TURNO'] = 'RENÚNCIA/FALECIMENTO/CASSAÇÃO ANTES A ELEIÇÃO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '10', 'DESC_SIT_TOT_TURNO'] = 'RENÚNCIA/FALECIMENTO/CASSAÇÃO APÓS A ELEIÇÃO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '11', 'DESC_SIT_TOT_TURNO'] = 'REGISTRO NEGADO ANTES DA ELEIÇÃO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '12', 'DESC_SIT_TOT_TURNO'] = 'REGISTRO NEGADO APÓS A ELEIÇÃO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '13', 'DESC_SIT_TOT_TURNO'] = 'INDEFERIDO COM RECURSO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '14', 'DESC_SIT_TOT_TURNO'] = 'CASSADO COM RECURSO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '15', 'DESC_SIT_TOT_TURNO'] = 'SUBSTITUÍDO'
    df.loc[df['COD_SIT_TOT_TURNO'] == '16', 'DESC_SIT_TOT_TURNO'] = 'RENÚNCIA/FALECIMENTO COM SUBSTITUIÇÃO'

    return df


class SitTotTurnoFix1998:

    def check(self, item):
        return item['year'] == 1998 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '206'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '309'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '502'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7', 'COD_SIT_TOT_TURNO'] = '7010'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8', 'COD_SIT_TOT_TURNO'] = '8011'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9', 'COD_SIT_TOT_TURNO'] = '9012'  # 9 -> 12

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '206', 'COD_SIT_TOT_TURNO'] = '6'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '309', 'COD_SIT_TOT_TURNO'] = '9'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '502', 'COD_SIT_TOT_TURNO'] = '2'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7010', 'COD_SIT_TOT_TURNO'] = '10'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8011', 'COD_SIT_TOT_TURNO'] = '11'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9012', 'COD_SIT_TOT_TURNO'] = '12'  # 9 -> 12

        return apply_description(df)


class SitTotTurnoFix2000:

    def check(self, item):
        return item['year'] == 2000 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '206'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '309'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '502'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7', 'COD_SIT_TOT_TURNO'] = '7010'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8', 'COD_SIT_TOT_TURNO'] = '8011'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9', 'COD_SIT_TOT_TURNO'] = '9012'  # 9 -> 12
        df.loc[df['COD_SIT_TOT_TURNO'] == '10', 'COD_SIT_TOT_TURNO'] = '1016'  # 10 -> 16

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '206', 'COD_SIT_TOT_TURNO'] = '6'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '309', 'COD_SIT_TOT_TURNO'] = '9'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '502', 'COD_SIT_TOT_TURNO'] = '2'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7010', 'COD_SIT_TOT_TURNO'] = '10'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8011', 'COD_SIT_TOT_TURNO'] = '11'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9012', 'COD_SIT_TOT_TURNO'] = '12'  # 9 -> 12
        df.loc[df['COD_SIT_TOT_TURNO'] == '1016', 'COD_SIT_TOT_TURNO'] = '16'  # 10 -> 16

        return apply_description(df)


class SitTotTurnoFix2002:

    def check(self, item):
        return item['year'] == 2002 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        df.loc[df['COD_SIT_TOT_TURNO'] == '-3', 'COD_SIT_TOT_TURNO'] = '-1'  # -3 -> -1

        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '206'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '309'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '502'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7', 'COD_SIT_TOT_TURNO'] = '7010'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8', 'COD_SIT_TOT_TURNO'] = '8011'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9', 'COD_SIT_TOT_TURNO'] = '9012'  # 9 -> 12

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '206', 'COD_SIT_TOT_TURNO'] = '6'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '309', 'COD_SIT_TOT_TURNO'] = '9'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '502', 'COD_SIT_TOT_TURNO'] = '2'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7010', 'COD_SIT_TOT_TURNO'] = '10'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8011', 'COD_SIT_TOT_TURNO'] = '11'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9012', 'COD_SIT_TOT_TURNO'] = '12'  # 9 -> 12

        return apply_description(df)


class SitTotTurnoFix2004:

    def check(self, item):
        return item['year'] == 2004 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        df.loc[df['COD_SIT_TOT_TURNO'] == '-3', 'COD_SIT_TOT_TURNO'] = '-1'  # -3 -> -1

        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '206'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '309'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '502'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7', 'COD_SIT_TOT_TURNO'] = '7010'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8', 'COD_SIT_TOT_TURNO'] = '8011'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9', 'COD_SIT_TOT_TURNO'] = '9012'  # 9 -> 12
        df.loc[df['COD_SIT_TOT_TURNO'] == '10', 'COD_SIT_TOT_TURNO'] = '1016'  # 10 -> 16

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '206', 'COD_SIT_TOT_TURNO'] = '6'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '309', 'COD_SIT_TOT_TURNO'] = '9'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '502', 'COD_SIT_TOT_TURNO'] = '2'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7010', 'COD_SIT_TOT_TURNO'] = '10'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8011', 'COD_SIT_TOT_TURNO'] = '11'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9012', 'COD_SIT_TOT_TURNO'] = '12'  # 9 -> 12
        df.loc[df['COD_SIT_TOT_TURNO'] == '1016', 'COD_SIT_TOT_TURNO'] = '16'  # 10 -> 16

        return apply_description(df)


class SitTotTurnoFix2006:

    def check(self, item):
        return item['year'] == 2006 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '206'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '309'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '502'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7', 'COD_SIT_TOT_TURNO'] = '7010'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8', 'COD_SIT_TOT_TURNO'] = '8011'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9', 'COD_SIT_TOT_TURNO'] = '9012'  # 9 -> 12

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '206', 'COD_SIT_TOT_TURNO'] = '6'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '309', 'COD_SIT_TOT_TURNO'] = '9'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '502', 'COD_SIT_TOT_TURNO'] = '2'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7010', 'COD_SIT_TOT_TURNO'] = '10'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8011', 'COD_SIT_TOT_TURNO'] = '11'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9012', 'COD_SIT_TOT_TURNO'] = '12'  # 9 -> 12

        return apply_description(df)


class SitTotTurnoFix2008:

    def check(self, item):
        return item['year'] == 2008 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '206'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '309'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '502'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7', 'COD_SIT_TOT_TURNO'] = '7010'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8', 'COD_SIT_TOT_TURNO'] = '8011'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9', 'COD_SIT_TOT_TURNO'] = '9012'  # 9 -> 12
        df.loc[df['COD_SIT_TOT_TURNO'] == '10', 'COD_SIT_TOT_TURNO'] = '1015'  # 10 -> 15

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '206', 'COD_SIT_TOT_TURNO'] = '6'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '309', 'COD_SIT_TOT_TURNO'] = '9'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '502', 'COD_SIT_TOT_TURNO'] = '2'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7010', 'COD_SIT_TOT_TURNO'] = '10'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8011', 'COD_SIT_TOT_TURNO'] = '11'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9012', 'COD_SIT_TOT_TURNO'] = '12'  # 9 -> 12
        df.loc[df['COD_SIT_TOT_TURNO'] == '1015', 'COD_SIT_TOT_TURNO'] = '15'  # 10 -> 15

        return apply_description(df)


class SitTotTurnoFix2010:

    def check(self, item):
        return item['year'] == 2010 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '206'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '309'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '502'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7', 'COD_SIT_TOT_TURNO'] = '7010'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8', 'COD_SIT_TOT_TURNO'] = '8011'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9', 'COD_SIT_TOT_TURNO'] = '9012'  # 9 -> 12
        df.loc[df['COD_SIT_TOT_TURNO'] == '10', 'COD_SIT_TOT_TURNO'] = '1015'  # 10 -> 15
        df.loc[df['COD_SIT_TOT_TURNO'] == '11', 'COD_SIT_TOT_TURNO'] = '1113'  # 11 -> 13
        df.loc[df['COD_SIT_TOT_TURNO'] == '12', 'COD_SIT_TOT_TURNO'] = '1214'  # 12 -> 14

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '206', 'COD_SIT_TOT_TURNO'] = '6'  # 2 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '309', 'COD_SIT_TOT_TURNO'] = '9'  # 3 -> 9
        df.loc[df['COD_SIT_TOT_TURNO'] == '502', 'COD_SIT_TOT_TURNO'] = '2'  # 5 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5
        df.loc[df['COD_SIT_TOT_TURNO'] == '7010', 'COD_SIT_TOT_TURNO'] = '10'  # 7 -> 10
        df.loc[df['COD_SIT_TOT_TURNO'] == '8011', 'COD_SIT_TOT_TURNO'] = '11'  # 8 -> 11
        df.loc[df['COD_SIT_TOT_TURNO'] == '9012', 'COD_SIT_TOT_TURNO'] = '12'  # 9 -> 12
        df.loc[df['COD_SIT_TOT_TURNO'] == '1015', 'COD_SIT_TOT_TURNO'] = '15'  # 10 -> 15
        df.loc[df['COD_SIT_TOT_TURNO'] == '1113', 'COD_SIT_TOT_TURNO'] = '13'  # 11 -> 13
        df.loc[df['COD_SIT_TOT_TURNO'] == '1214', 'COD_SIT_TOT_TURNO'] = '14'  # 12 -> 14

        return apply_description(df)


class SitTotTurnoFix2012:

    def check(self, item):
        return item['year'] == 2012 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '203'  # 2 -> 3
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '302'  # 3 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '506'  # 5 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '203', 'COD_SIT_TOT_TURNO'] = '3'  # 2 -> 3
        df.loc[df['COD_SIT_TOT_TURNO'] == '302', 'COD_SIT_TOT_TURNO'] = '2'  # 3 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '506', 'COD_SIT_TOT_TURNO'] = '6'  # 5 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5

        return apply_description(df)

class SitTotTurnoFix2014:

    def check(self, item):
        return item['year'] == 2014 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '203'  # 2 -> 3
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '302'  # 3 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '506'  # 5 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '203', 'COD_SIT_TOT_TURNO'] = '3'  # 2 -> 3
        df.loc[df['COD_SIT_TOT_TURNO'] == '302', 'COD_SIT_TOT_TURNO'] = '2'  # 3 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '506', 'COD_SIT_TOT_TURNO'] = '6'  # 5 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5

        return apply_description(df)


class SitTotTurnoFix2016:

    def check(self, item):
        return item['year'] == 2016 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '203'  # 2 -> 3
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '302'  # 3 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '506'  # 5 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '203', 'COD_SIT_TOT_TURNO'] = '3'  # 2 -> 3
        df.loc[df['COD_SIT_TOT_TURNO'] == '302', 'COD_SIT_TOT_TURNO'] = '2'  # 3 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '506', 'COD_SIT_TOT_TURNO'] = '6'  # 5 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5

        return apply_description(df)


class SitTotTurnoFix2018:

    def check(self, item):
        return item['year'] == 2018 and item['database'] == 'candidatos'

    def apply(self, df: pd.DataFrame):
        # Move all COD to AUX
        df.loc[df['COD_SIT_TOT_TURNO'] == '2', 'COD_SIT_TOT_TURNO'] = '203'  # 2 -> 3
        df.loc[df['COD_SIT_TOT_TURNO'] == '3', 'COD_SIT_TOT_TURNO'] = '302'  # 3 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '5', 'COD_SIT_TOT_TURNO'] = '506'  # 5 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '6', 'COD_SIT_TOT_TURNO'] = '605'  # 6 -> 5

        # Apply COD changes
        df.loc[df['COD_SIT_TOT_TURNO'] == '203', 'COD_SIT_TOT_TURNO'] = '3'  # 2 -> 3
        df.loc[df['COD_SIT_TOT_TURNO'] == '302', 'COD_SIT_TOT_TURNO'] = '2'  # 3 -> 2
        df.loc[df['COD_SIT_TOT_TURNO'] == '506', 'COD_SIT_TOT_TURNO'] = '6'  # 5 -> 6
        df.loc[df['COD_SIT_TOT_TURNO'] == '605', 'COD_SIT_TOT_TURNO'] = '5'  # 6 -> 5

        return apply_description(df)
