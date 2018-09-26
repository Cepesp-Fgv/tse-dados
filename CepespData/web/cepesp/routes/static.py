from flask import render_template, request, session

from web.cepesp.utils.session import get_locale


def home():
    session['back'] = request.path
    return render_template("home.html", page=0, lang=get_locale())


def about():
    session['back'] = request.path
    return render_template("about.html", page=4, lang=get_locale())
