from flask import render_template, request, session, redirect

from web.cepesp.config import APP_ENV
from web.cepesp.utils.session import get_locale


def home():
    if APP_ENV == 'master':
        return redirect('http://fgv.cepesp.io')
    else:
        session['back'] = request.path
        return render_template("home.html", page=0, lang=get_locale())


def about():
    session['back'] = request.path
    return render_template("about.html", page=4, lang=get_locale())
