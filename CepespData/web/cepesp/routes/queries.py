from flask import session, request, render_template

from web.cepesp.candidatos.options import CandidatosOptions
from web.cepesp.legendas.options import LegendasOptions
from web.cepesp.tse.options import TSEVotosOptions
from web.cepesp.utils.data import get_years
from web.cepesp.utils.mun import get_uf_list, get_mun_list
from web.cepesp.utils.session import get_locale
from web.cepesp.votos.options import VotosMunOptions


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


def consulta_votos():
    session['back'] = request.path
    options = VotosMunOptions()
    show = len(list(request.args.values())) > 0

    return render_template(
        "votosmun.html",
        options=options,
        page=4,
        show=show,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        lang=get_locale()
    )
