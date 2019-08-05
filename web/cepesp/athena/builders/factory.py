from web.cepesp.utils.request import trim
from web.cepesp.athena.builders.candidates_assets import CandidateAssetsQueryBuilder
from web.cepesp.athena.builders.elections import ElectionsQueryBuilder, SummaryElectionsQueryBuilder
from web.cepesp.athena.builders.others import VotesQueryBuilder, CandidatesCoalitionsQueryBuilder
from web.cepesp.athena.builders.party_affiliations import PartyAffiliationsQueryBuilder
from web.cepesp.athena.builders.secretaries import SecretariesQueryBuilder
from web.cepesp.athena.builders.utils import arg, opt


def build_query(**options):
    table = arg(options, 'table')
    pol = opt(options, 'pol', 0)

    if table == 'tse' and pol != 4:
        builder = ElectionsQueryBuilder(**options)
    elif table == 'tse' and pol == 4:
        builder = SummaryElectionsQueryBuilder(**options)
    elif table == 'votos':
        builder = VotesQueryBuilder(**options)
    elif table == 'bem_candidato':
        builder = CandidateAssetsQueryBuilder(**options)
    elif table == 'filiados':
        builder = PartyAffiliationsQueryBuilder(**options)
    elif table == 'secretarios':
        builder = SecretariesQueryBuilder(**options)
    elif table in ['candidatos', 'legendas']:
        builder = CandidatesCoalitionsQueryBuilder(**options)
    else:
        raise KeyError(f'Invalid table {table} supplied')

    return trim(builder.build())
