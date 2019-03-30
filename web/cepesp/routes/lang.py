from flask import session
from flask_babel import refresh
from werkzeug.utils import redirect

from web.cepesp.utils.session import back


def lang(locale):
    if locale in ['pt', 'en']:
        session['locale'] = locale
        refresh()
    return redirect(back())