from flask import session, request, render_template

from web.cepesp.athena.options import AthenaQueryOptions
from web.cepesp.utils.data import get_years
from web.cepesp.utils.mun import get_uf_list, get_mun_list
from web.cepesp.utils.session import get_locale


def consulta_tse():
    session['back'] = request.path
    options = AthenaQueryOptions('tse')
    show = len(list(request.args.values())) > 0

    return render_template(
        "tse.html",
        options=options,
        page=1,
        show=show,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        mun_list=get_mun_list(),
        lang=get_locale()
    )


def consulta_candidatos():
    session['back'] = request.path
    options = AthenaQueryOptions('candidatos')
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


def consulta_legendas():
    session['back'] = request.path
    options = AthenaQueryOptions('legendas')
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


def consulta_votos():
    session['back'] = request.path
    options = AthenaQueryOptions('votos')
    show = len(list(request.args.values())) > 0

    return render_template(
        "votos.html",
        options=options,
        page=4,
        show=show,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        lang=get_locale()
    )


def consulta_bem_candidato():
    session['back'] = request.path
    options = AthenaQueryOptions('bem_candidato')
    show = len(list(request.args.values())) > 0

    return render_template(
        "bem_candidato.html",
        options=options,
        page=6,
        show=show,
        years=[2018, 2016, 2014, 2012, 2010, 2008, 2006],
        uf_list=get_uf_list(),
        lang=get_locale()
    )
