import bugsnag
import flask
from flask import render_template
from werkzeug.exceptions import HTTPException

from web.cepesp.config import APP_DEBUG
from web.cepesp.utils.request import request_wants_json
import logging


def handle_error(e):
    code = e.code if isinstance(e, HTTPException) else 500
    message = e.description if isinstance(e, HTTPException) else str(e)

    if APP_DEBUG and code >= 500:
        logging.exception(message)

    bugsnag.notify(e)

    if request_wants_json():
        return flask.jsonify({'error': message, 'code': code}), code
    elif code == 404:
        return render_template('errors/404.html'), code
    else:
        return render_template('errors/500.html', message=message, code=code), code
