class SiglaUEFix:

    def check(self, item):
        if item['database'] == 'votos' and item['uf'] == 'ZZ':
            return False

        return item['database'] in ['votos', 'legendas', 'candidatos']

    def apply(self, df):
        df.loc[df.CODIGO_CARGO == '1', 'SIGLA_UE'] = 'BR'
        df.loc[df.CODIGO_CARGO == '3', 'SIGLA_UE'] = df['SIGLA_UF']
        df.loc[df.CODIGO_CARGO == '5', 'SIGLA_UE'] = df['SIGLA_UF']
        df.loc[df.CODIGO_CARGO == '6', 'SIGLA_UE'] = df['SIGLA_UF']
        df.loc[df.CODIGO_CARGO == '7', 'SIGLA_UE'] = df['SIGLA_UF']

        return df
