from botocore.exceptions import ClientError
from flask import request, jsonify
from flask_babel import gettext
from werkzeug.exceptions import BadRequest, NotFound

from web.cepesp.athena.client import AthenaQueryFailed
from web.cepesp.athena.options import AthenaQueryOptions, AthenaResultOptions
from web.cepesp.athena.query import AthenaQuery, QueryNotFoundException
from web.cepesp.config import API_PYTHON_VERSION, API_R_VERSION, APP_ENV
from web.cepesp.routes.lang import lang
from web.cepesp.utils.analytics import track_event
from web.cepesp.utils.output import ResponseConverter


def athena_api(table):
    lang(request.args.get('lang', 'pt'))

    options = AthenaQueryOptions(table).to_dict()
    track_event("API", options['name'])

    return _athena_response(options, wait=True)


def athena_query_api():
    lang(request.args.get('lang', 'pt'))

    query = AthenaQuery()
    options = AthenaQueryOptions()
    track_event("API", options.name)

    return jsonify(query.get_info(options.to_dict()))


def athena_status_api():
    lang(request.args.get('lang', 'pt'))

    query = AthenaQuery()
    options = AthenaResultOptions()
    options.validate()

    return jsonify(query.get_status(options.to_dict()))


def athena_result_api():
    lang(request.args.get('lang', 'pt'))

    options = AthenaResultOptions()
    options.validate()
    return _athena_response(options.to_dict())


def columns_api():
    lang(request.args.get('lang', 'pt'))

    options = AthenaQueryOptions()
    return jsonify({
        'columns': options.all_columns,
        'translated_columns': {c: gettext('columns.' + c) for c in options.all_columns},
        'default_columns': options.default_columns,
        'descriptions': {c: gettext('descriptions.' + c) for c in options.all_columns}
    })


def _athena_response(options, wait=False):
    _validate_api_version()

    try:
        query = AthenaQuery()
        info = query.get_info(options, wait)
        converter = ResponseConverter(info['name'])

        if options['length'] > 0:
            df = query.get_df(options)
            if options['format'] == 'json':
                return converter.to_json(df, options['start'])
            else:
                return converter.to_csv(df, options['separator'])
        else:
            stream = query.get_stream(options)
            return converter.to_stream(stream)

    except ClientError as e:
        raise BadRequest(str(e))
    except AthenaQueryFailed as e:
        raise BadRequest(str(e))
    except QueryNotFoundException as e:
        raise NotFound(str(e))


def _validate_api_version():
    py_ver = request.args.get('py_ver')
    r_ver = request.args.get('r_ver')
    ignore_version = request.args.get('ignore_version')

    if not ignore_version and APP_ENV != 'test':
        if py_ver and py_ver != '*' and API_PYTHON_VERSION != '*' and py_ver != API_PYTHON_VERSION:
            raise BadRequest('Invalid API Version. Please, update your python api library to the latest version.')

        if r_ver and r_ver != '*' and API_R_VERSION != '*' and r_ver != API_R_VERSION:
            raise BadRequest('Invalid API Version. Please, update your R api library to the latest version.')

        if (not py_ver) and (not r_ver):
            raise BadRequest(
                f'Please, provide a valid api version. (r_ver: {API_R_VERSION} | py_ver: {API_PYTHON_VERSION})'
            )
