from flask import make_response

from web.cepesp.athena.builders.factory import build_query
from web.cepesp.athena.options import AthenaQueryOptions


def sql():
    options = AthenaQueryOptions()
    response = make_response(build_query(**options.__dict__))
    response.headers['Content-Disposition'] = f'attachment; filename={options.name}.sql'
    response.mimetype = 'text/txt'

    return response
