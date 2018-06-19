import os

from flask import Flask, make_response, session, request, url_for, redirect
from flask import render_template
from flask_babel import Babel, refresh

from lib.candidatos.options import CandidatosOptions
from lib.candidatos.processors import CandidatosQuery
from lib.legendas.options import LegendasOptions
from lib.legendas.processors import LegendasQuery
from lib.tse.options import TSEVotosOptions
from lib.tse.processors import TSEVotosQuery
from lib.utils.data import COD_SIT, get_years
from lib.utils.mun import get_uf_list, get_mun_list
from lib.utils.output import ResponseConverter, CachedQuery
from lib.votos.options import VotosMunOptions
from lib.votos.processors import VotosMunQuery

application = Flask(__name__)
application.secret_key = "DYp8IKYCEO7VjqcBbyGg2tcKYzDKxgbkkLwihAXD448="
babel = Babel(application)


@babel.localeselector
def get_locale():
    return session.get('locale', 'pt')


def back(default='/'):
    return session.get('back', default)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(application.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)

    return url_for(endpoint, **values)


@application.template_filter('asset')
def asset_filter(fl):
    return dated_url_for('static', filename=fl)


@application.route('/lang/<locale>')
def lang(locale):
    if locale in ['pt', 'en']:
        session['locale'] = locale
        refresh()
    return redirect(back())


@application.route('/pt')
def lang_pt():
    lang('pt')


@application.route('/en')
def lang_en():
    lang('en')


# @app.route('/')
@application.errorhandler(404)
def not_found(e):
    return render_template("404.html", status=404)


@application.route('/')
def home():
    session['back'] = request.path
    return render_template("home.html", page=0, lang=get_locale())


@application.route('/sobre')
def about():
    return render_template("about.html", page=2, lang=get_locale())


@application.route('/consulta/tse')
def consulta_tse():
    session['back'] = request.path
    options = TSEVotosOptions()
    show = len(list(request.args.values())) > 0

    return render_template(
        "query.html",
        options=options,
        page=1,
        show=show,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        mun_list=get_mun_list(),
        lang=get_locale()
    )


@application.route('/consulta/candidatos')
def consulta_candidatos():
    session['back'] = request.path
    options = CandidatosOptions()
    show = len(list(request.args.values())) > 0

    return render_template(
        "candidatos.html",
        options=options,
        page=2,
        show=show,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        lang=get_locale()
    )


@application.route('/consulta/legendas')
def consulta_legendas():
    session['back'] = request.path
    options = LegendasOptions()
    show = len(list(request.args.values())) > 0

    return render_template(
        "legendas.html",
        options=options,
        page=3,
        show=show,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        lang=get_locale()
    )


@application.route('/consulta/votos')
def consulta_votos():
    session['back'] = request.path
    options = VotosMunOptions()
    show = len(list(request.args.values())) > 0

    return render_template(
        "votosmun.html",
        options=options,
        page=5,
        show=show,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        lang=get_locale()
    )


@application.route('/consulta/tse/sql')
def consulta_sql():
    cargo = request.args.get('cargo', 1, int)
    ano = request.args.get('ano', 2014, int)
    response = make_response(render_template(
        "sql/joins.html",
        cargos=[cargo],
        anos=[ano],
        cod_sit=COD_SIT,
        agregacoes=["micro", "mun", "munzona"]
    ))
    response.headers['Content-Disposition'] = 'attachment; filename=sql.txt'
    response.mimetype = 'text/txt'
    return response


@application.route('/sql/joins')
def sql_join():
    # cargos = [1, 3, 5, 6, 7, 8]
    cargos = [11]
    response = make_response(render_template(
        "sql/joins.html",
        cargos=cargos,
        # anos=[1998, 2002, 2006, 2010, 2014],
        anos=[2012],
        cod_sit=COD_SIT,
        agregacoes=["micro", "mun", "munzona"]
    ))
    response.headers['Content-Disposition'] = 'attachment; filename=sql.txt'
    response.mimetype = 'text/txt'
    return response


@application.route('/sql/consolidado')
def sql_consolidado():
    cargos = [11, 13]
    response = make_response(render_template(
        "sql/consolidado.html",
        cargos=cargos,
        anos=[2012],
    ))
    response.headers['Content-Disposition'] = 'attachment; filename=sql.txt'
    response.mimetype = 'text/txt'
    return response


@application.route('/sql/create')
def sql_create():
    response = make_response(render_template(
        "sql/create.html",
        # anos=[1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016]
        anos=[2012]
    ))
    response.headers['Content-Disposition'] = 'attachment; filename=sql.txt'
    response.mimetype = 'text/txt'
    return response


# region API
@application.route('/api/consulta/tse')
def tse_api():
    return api(TSEVotosQuery())


@application.route('/api/consulta/candidatos')
def candidatos_api():
    return api(CandidatosQuery())


@application.route('/api/consulta/legendas')
def legendas_api():
    return api(LegendasQuery())


@application.route('/api/consulta/votos')
def votos_api():
    return api(VotosMunQuery())


def api(query):
    lang(request.args.get('lang', 'pt'))

    converter = ResponseConverter(query.options.name)
    query = CachedQuery(query)
    (result, total_count, filtered_count) = query.get()

    return converter.convert(result, total_count, filtered_count)


# endregion


if __name__ == "__main__":
    application.debug = True
    application.run()
