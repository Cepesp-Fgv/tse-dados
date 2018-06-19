from flask import session, request

from lib.utils.data import get_years


def get_selected_columns(default_columns, available_columns):
    columns = [str(item) for item in request.args.getlist("selected_columns[]")]

    if len(columns) == 0:
        columns = [str(item) for item in request.args.getlist("selected_columns")]

    key = 'columns_' + request.path.split('/')[-1]

    if len(columns) == 0 and key in session:
        columns = [c for c in session[key] if c in available_columns]

    if len(columns) == 0:
        columns = default_columns

    session[key] = columns

    return columns


def get_request_years(selected_job):
    lista = request.args.getlist("anos[]", int)
    if len(lista) > 0:
        return lista
    else:
        return [int(a) for a in
                request.args.get("anos", request.args.get("ano", str(get_years(selected_job)[0]))).split(',')]


def get_request_filters(selected_columns):
    filters = {}

    # DATA TABLE FILTERS
    for i, column in enumerate(selected_columns):
        for selected_name in selected_columns:
            search = request.args.get("columns[%d][search][value]" % i)
            name = request.args.get("columns[%d][name]" % i)
            if selected_name == name and search:
                filters[name] = str(search)

    return filters
