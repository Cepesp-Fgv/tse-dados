from flask import render_template, request, session, redirect

from web.cepesp.config import APP_ENV
from web.cepesp.utils.session import get_locale


def home():
    host = request.headers['Host']

    if APP_ENV == 'master' and 'cepesp.io' in host:
        return redirect('http://www.cepesp.io')
    else:
        session['back'] = request.path
        return render_template("home.html", page=0, lang=get_locale())


def others():
    session['back'] = request.path
    return render_template("others.html", page=0, lang=get_locale())


def about():
    session['back'] = request.path
    return render_template("about.%s.html" % get_locale(), page=1, lang=get_locale())


def about_state_secretaries():
    session['back'] = request.path
    return render_template("about_secretarios.%s.html" % get_locale(), page=1, lang=get_locale())