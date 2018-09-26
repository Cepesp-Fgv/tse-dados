import os

from etl.fixes.AppendExtraJobs2014 import AppendExtraJobs2014
from etl.fixes.CheckJoinCandidatosLegendas import CheckJoinCandidatosLegendas
from etl.fixes.DescSitTotTurnoCandidato import DescSitTotTurnoCandidato
from etl.fixes.DescricaoEleicaoFix2010 import DescricaoEleicaoFix2010
from etl.fixes.DescricaoEleicaoFix2014 import DescricaoEleicaoFix2014
from etl.fixes.FixCodigoCorRaca import FixCodigoCorRaca
from etl.fixes.FixEmailCandidato import FixEmailCandidato
from etl.fixes.FixSequenciaColigacao2010 import FixSequenciaColigacao2010
from etl.fixes.FixSequencial2014Legendas import FixSequencial2014Legendas

from dotenv import load_dotenv

base = os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(base, '../.env'))

OUTPUT = os.path.join(base, 'output')
AUX_MUN = os.path.join(base, 'aux_mun_code.csv.gz')
YEARS = [2014, 2010]
JOBS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
DATABASES = ["votos", "candidatos", "legendas"]
FIXES = [
    AppendExtraJobs2014(os.path.join(base, 'candidatos_2014_semvotos.gz')),
    DescricaoEleicaoFix2014(),
    DescSitTotTurnoCandidato(),
    FixSequencial2014Legendas(),
    FixCodigoCorRaca(),
    FixEmailCandidato(),
    CheckJoinCandidatosLegendas(),
    DescricaoEleicaoFix2010(),
    FixSequenciaColigacao2010(os.path.join(OUTPUT, 'processed/candidato_2010.gz'))
]

MYSQL = {
    "host": os.getenv('ETL_DB_HOST', 'localhost'),
    "port": os.getenv('ETL_DB_PORT', '3306'),
    "user": os.getenv('ETL_DB_USERNAME', 'root'),
    "password": os.getenv('ETL_DB_PASSWORD'),
    "database": os.getenv('ETL_DB_DATABASE', 'cepespdata')
}
