import os

from dotenv import load_dotenv

from etl.fixes.AppendExtraJobs2014 import AppendExtraJobs2014
from etl.fixes.DescricaoEleicaoFix2010 import DescricaoEleicaoFix2010
from etl.fixes.DescricaoEleicaoFix2014 import DescricaoEleicaoFix2014
from etl.fixes.FixCodMunTSE import FixCodMunTSE
from etl.fixes.FixCodigoCorRaca import FixCodigoCorRaca
from etl.fixes.FixComposicaoLegendaCandidato import FixComposicaoLegendaCandidato2006
from etl.fixes.FixEmailCandidato import FixEmailCandidato
from etl.fixes.FixSequenciaColigacao2010 import FixSequenciaColigacao2010
from etl.fixes.FixSequencial2014Legendas import FixSequencial2014Legendas
from etl.fixes.FixTituloEleitor import FixTituloEleitor
from etl.fixes.SiglaUEFix import SiglaUEFix
from etl.fixes.SitTotTurnoFix import *

base = os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(base, '../.env'))

OUTPUT = os.path.join(base, 'output')
AUX_MUN = os.path.join(base, 'aux_mun_code.csv.gz')
YEARS = [2010]
JOBS = [1]
DATABASES = ["votos", "candidatos", "legendas"]
FIXES = [
    AppendExtraJobs2014(os.path.join(base, 'candidatos_2014_semvotos.gz')),
    DescricaoEleicaoFix2014(),
    FixSequencial2014Legendas(),
    FixCodigoCorRaca(),
    FixEmailCandidato(),
    DescricaoEleicaoFix2010(),
    FixSequenciaColigacao2010(os.path.join(OUTPUT, 'processed/candidato_2010.gz')),
    FixTituloEleitor(),
    FixCodMunTSE(),
    FixComposicaoLegendaCandidato2006(os.path.join(OUTPUT, 'processed/legendas_2006.gz'),
                                      os.path.join(OUTPUT, 'processed/legendas_2006_presidente.gz')),

    SitTotTurnoFix1998(),
    SitTotTurnoFix2000(),
    SitTotTurnoFix2002(),
    SitTotTurnoFix2004(),
    SitTotTurnoFix2006(),
    SitTotTurnoFix2008(),
    SitTotTurnoFix2010(),
    SitTotTurnoFix2012(),
    SitTotTurnoFix2014(),
    SitTotTurnoFix2016(),
    SitTotTurnoFix2018(),

    SiglaUEFix()
]
