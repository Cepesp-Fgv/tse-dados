from flask import make_response

from web.cepesp.athena.options import AthenaQueryOptions
from web.cepesp.athena.query import AthenaQuery


def sql():
    query = AthenaQuery()
    options = AthenaQueryOptions()
    response = make_response(query.build_query(options.__dict__))
    response.headers['Content-Disposition'] = f'attachment; filename={options.name}.sql'
    response.mimetype = 'text/txt'

    return response
