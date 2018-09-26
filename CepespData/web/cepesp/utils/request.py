from typing import Type

from flask import request

from web.cepesp.utils.data import get_years
from web.cepesp.utils.session import session_selected_columns, set_session_selected_columns


def request_get_list(key, item_type: Type = str, split=None, default=None):
    items = [item_type(item) for item in request.args.getlist(key + "[]")]

    value = request.args.getlist(key)
    if value and len(items) == 0:
        items = [item_type(item) for item in value if split not in item]

    value = request.args.get(key)
    if split and value:
        value = value.split(split)
        if len(value) > len(items):
            items = [item_type(item) for item in value]

    if default and len(items) == 0:
        return default

    return items


def request_selected_columns():
    columns = request_get_list("selected_columns")

    if len(columns) == 0:
        columns = request_get_list("c", split=',')

    return columns


def get_selected_columns(default_columns, available_columns):
    columns = request_selected_columns()

    if len(columns) == 0:
        columns = session_selected_columns(available_columns)

    if len(columns) == 0:
        columns = default_columns

    set_session_selected_columns(columns)

    return columns


def get_request_years(selected_job):
    default_year = get_years(selected_job)[0]
    years = request_get_list("ano", int, ',', [default_year])
    years = request_get_list("anos", int, ',', years)

    return years


def get_request_filters(selected_columns):
    filters = {}

    for column in selected_columns:
        value = request.args.get("filters[%s]" % column)
        if value:
            filters[column] = value

    if len(filters) == 0:
        # DATA TABLE FILTERS
        for i, column in enumerate(selected_columns):
            for selected_name in selected_columns:
                search = request.args.get("columns[%d][search][value]" % i)
                name = request.args.get("columns[%d][name]" % i)
                if selected_name == name and search:
                    filters[name] = str(search)

    return filters
