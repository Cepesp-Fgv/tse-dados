class BemCandidatoSiglaUEFix:

    def check(self, item):
        return item['database'] == 'bem_candidato' and item["year"] < 2014

    def apply(self, df):
        df['SIGLA_UE'] = df['SIGLA_UF']

        return df