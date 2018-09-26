import flask
from werkzeug.exceptions import HTTPException

from web.cepesp.config import APP_DEBUG

ERRORS = {
    404: 'Not Found',
    405: 'Method Not Allowed',
    414: 'URI Too Long',
    500: 'Internal Server Error',
    503: 'Service Unavailable',
}


def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code

    if not APP_DEBUG:
        if code in ERRORS.keys():
            message = ERRORS[code]
        else:
            message = ERRORS[500]

        return flask.Response(message, code)
    else:
        raise e
