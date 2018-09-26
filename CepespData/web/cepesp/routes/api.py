from flask import request

from web.cepesp.athena.query import AthenaQuery
from web.cepesp.candidatos.processors import CandidatosQuery
from web.cepesp.legendas.processors import LegendasQuery
from web.cepesp.routes.lang import lang
from web.cepesp.tse.processors import TSEVotosQuery
from web.cepesp.utils.analytics import track_event
from web.cepesp.utils.output import ResponseConverter, CachedQuery
from web.cepesp.votos.processors import VotosMunQuery


def tse_api():
    query = TSEVotosQuery()
    years = list(map(str, query.options.years))

    if query.options.pol == 2 and ('2010' in years or '2014' in years):
        return athena_api()
    else:
        return api(query)


def candidatos_api():
    return api(CandidatosQuery())


def legendas_api():
    return api(LegendasQuery())


def votos_api():
    return api(VotosMunQuery())


def athena_api():
    lang(request.args.get('lang', 'pt'))

    query = AthenaQuery()
    track_event("API", query.options.name)

    converter = ResponseConverter(query.options.name)
    converter.paginate_inner = False

    if converter.length > 0:
        df = query.get(converter.length, converter.start)
        total = converter.length * 5
        return converter.convert(df, total, total)
    else:
        stream = query.get_stream()
        return converter.convert_stream(stream)


def api(query):
    lang(request.args.get('lang', 'pt'))

    track_event("API", query.options.name)

    converter = ResponseConverter(query.options.name)
    query = CachedQuery(query)
    (result, total_count, filtered_count) = query.get()

    return converter.convert(result, total_count, filtered_count)
