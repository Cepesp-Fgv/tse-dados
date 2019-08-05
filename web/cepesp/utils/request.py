import re

from typing import Type

from flask import request

from web.cepesp.utils.data import get_years

rx = re.compile(r'[!?\\/\-\&\*\%\$\#\"\']+', flags=re.M | re.I)


def escape(value):
    return rx.sub('', value)


def trim(value):
    return re.sub('(\r|\n| )+', ' ', value).strip()


def request_get(key, default=None, item_type: Type = str):
    value = request.args.get(key)
    if value:
        return item_type(escape(value))
    else:
        return default


def request_get_list(key, item_type: Type = str, split=None, default=None):
    items = [item_type(item) for item in request.args.getlist(key + "[]")]

    value = request.args.getlist(key)
    if value and len(items) == 0:
        items = [item_type(escape(item)) for item in value if split not in item]

    value = request.args.get(key)
    if split and value:
        value = value.split(split)
        if len(value) > len(items):
            items = [item_type(escape(item)) for item in value]

    if default and len(items) == 0:
        return default

    return items


def request_selected_columns():
    columns = request_get_list("selected_columns")

    if len(columns) == 0:
        columns = request_get_list("c", split=',')

    columns = [escape(c) for c in columns]

    return columns


def get_selected_columns(default_columns, available_columns):
    columns = request_selected_columns()

    # if len(columns) == 0:
    #     columns = session_selected_columns(available_columns)

    if len(columns) == 0:
        columns = default_columns

    # set_session_selected_columns(columns)

    return columns


def get_request_years(selected_job):
    default_years = get_years(selected_job)
    years = request_get_list("ano", int, ',', default_years[0:1])
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


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html', 'text/csv'])

    return 'application/json' in [best, request.content_type]
