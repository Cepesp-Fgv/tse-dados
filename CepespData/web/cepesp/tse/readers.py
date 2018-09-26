import os
from urllib.parse import urlencode

import pandas as pd
from flask import request

from web.cepesp.candidatos.columns import CandidatosColumnsSelector
from web.cepesp.candidatos.processors import CandidatosQuery
from web.cepesp.legendas.columns import LegendasColumnsSelector
from web.cepesp.legendas.processors import LegendasQuery
from web.cepesp.tse.options import TSEVotosOptions
from web.cepesp.utils.data import resolve_conflicts
from web.cepesp.votos.columns import VotosMunColumnsSelector
from web.cepesp.votos.processors import VotosMunQuery

path_base = os.path.dirname(__file__)


class TSEDatabaseReader:

    def __init__(self, options):
        self.options = options
        self.server = "http://localhost:8000"

    def read(self) -> pd.DataFrame:
        url = self._build_url("consulta/tse")
        df = pd.read_csv(url, sep=';', dtype=str)
        df = df.rename(columns={
            'EMAIL_CANDIDATO': 'NM_EMAIL',
            'SEQUENCIA_COLIGACAO': 'SEQUENCIAL_COLIGACAO'
        })

        return df

    def _build_url(self, path):
        query = urlencode(self._build_args())
        return "{s}/api/{p}?{q}".format(s=self.server, p=path, q=query)

    def _build_args(self):
        return {
            'job': self.options.job,
            'years': ",".join(map(str, self.options.years)),
            'reg': self.options.reg,
            'pol': self.options.pol,
            'turn': self.options.turno if self.options.turno else 0,
            'uf': self.options.uf_filter if self.options.uf_filter else '',
            'mun': self.options.mun_filter if self.options.mun_filter else '',
            'filters': self.options.filters,
            'start': request.args.get("start", 0, int),
            'length': request.args.get("length", -1, int),
        }


class PresidentVotosCandidatosReader:

    def __init__(self, options):
        self.options = options

    def read(self) -> pd.DataFrame:
        votos = VotosMunQuery()
        votos.options.selected_columns = VotosMunColumnsSelector(self.options.reg).columns()

        candidatos = CandidatosQuery()
        candidatos.options.selected_columns = CandidatosColumnsSelector().columns()

        legendas = LegendasQuery()
        legendas.options.selected_columns = LegendasColumnsSelector().columns()

        [votos_df, _, _] = votos.get()
        [candidatos_df, _, _] = candidatos.get()
        [legendas_df, _, _] = legendas.get()

        return self.join(votos_df, candidatos_df, legendas_df)

    def join(self, votos, candidatos, legendas) -> pd.DataFrame:
        candidatos = candidatos.set_index(["NUMERO_PARTIDO", "NUM_TURNO", "ANO_ELEICAO"])
        legendas = legendas.set_index(["NUMERO_PARTIDO", "NUM_TURNO", "ANO_ELEICAO"])

        cand_leg = candidatos.merge(legendas, how="left", left_index=True, right_index=True).reset_index()
        cand_leg = resolve_conflicts(cand_leg)
        cand_leg = cand_leg.fillna("#NE#")

        votos = votos.set_index(["NUMERO_CANDIDATO", "NUM_TURNO", "ANO_ELEICAO"])
        cand_leg = cand_leg.set_index(["NUMERO_CANDIDATO", "NUM_TURNO", "ANO_ELEICAO"])

        vot_cand_leg = votos.merge(cand_leg, how="left", left_index=True, right_index=True).reset_index()
        vot_cand_leg = resolve_conflicts(vot_cand_leg)
        vot_cand_leg = vot_cand_leg.fillna("#NE#")
        vot_cand_leg['NOME_LEGENDA'] = vot_cand_leg['NOME_PARTIDO']
        vot_cand_leg = vot_cand_leg.rename(columns={
            'EMAIL_CANDIDATO': 'NM_EMAIL'
        })

        if not self.options.brancos:
            vot_cand_leg = vot_cand_leg[vot_cand_leg.NUMERO_CANDIDATO != '95']

        if not self.options.nulos:
            vot_cand_leg = vot_cand_leg[vot_cand_leg.NUMERO_CANDIDATO != '96']

        return vot_cand_leg


class TSEVotosReader:
    def __init__(self, options: TSEVotosOptions):
        self.options = options

    def read(self):
        df = None
        for y in self.options.years:
            if df is None:
                df = self._read_year(y)
            else:
                df = df.append(self._read_year(y))

        return df

    def _read_year(self, year):
        df = self._read_job(self.options.job, year)
        if self.options.job == 7:
            df = df.append(self._read_job(8, year))

        return df

    def _read_job(self, job, year):
        df = self._read(self.file_path(job, year))

        if os.path.exists(self.file_path(job, year, '000001_0.gz')):
            df = df.append(self._read(self.file_path(job, year, '000001_0.gz')))

        if os.path.exists(self.legenda_path(job, year)):
            df = df.append(self._read(self.legenda_path(job, year)))

        if self.options.pol != 4:
            if os.path.exists(self.brancos_path(job, year)) and self.options.brancos:
                df = df.append(self._read(self.brancos_path(job, year)))

            if os.path.exists(self.nulos_path(job, year)) and self.options.nulos:
                df = df.append(self._read(self.nulos_path(job, year)))

        if year == 2014 and job == 3:
            df = df[~df['DESCRICAO_ELEICAO'].str.contains("Suplementar", case=False, na=False)]

        if 'COD_MUN_TSE_NASCIMENTO' in df.columns:
            df['CODIGO_MUNICIPIO_NASCIMENTO'] = df['COD_MUN_TSE_NASCIMENTO']
        elif 'CODIGO_MUNICIPIO_NASCIMENTO' in df.columns:
            df['COD_MUN_TSE_NASCIMENTO'] = df['CODIGO_MUNICIPIO_NASCIMENTO']

        if 'NUMERO_PARTIDO' in self.options.selected_columns and job is 1:
            df['NUMERO_PARTIDO'] = df['NUMERO_CANDIDATO']

        return df

    def _read(self, file_path):
        return pd.read_csv(file_path, sep=';', dtype=str)

    def file_path(self, cargo, year, name='000000_0.gz'):
        if self.options.pol == 4:
            folder = 'detalhe'
        else:
            if self.options.reg == 7 or self.options.reg == 8:
                folder = 'munzona'
            elif self.options.reg == 6:
                folder = 'mun'
            else:
                folder = 'micro'

        return os.path.join(path_base, '../../storage/%s/%s/%s/%s' % (folder, year, cargo, name))

    def brancos_path(self, cargo, year):
        return self.file_path(cargo, year, 'brancos/000000_0.gz')

    def nulos_path(self, cargo, year):
        return self.file_path(cargo, year, 'nulos/000000_0.gz')

    def legenda_path(self, cargo, year):
        return self.file_path(cargo, year, 'legenda/000000_0.gz')
