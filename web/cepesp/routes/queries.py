from flask import session, request, render_template

from web.cepesp.athena.options import AthenaQueryOptions
from web.cepesp.utils.data import get_years
from web.cepesp.utils.mun import get_uf_list, get_mun_list, get_nomes_secretarios_list
from web.cepesp.utils.session import get_locale


def consulta_tse_2():
    session['back'] = request.path
    options = AthenaQueryOptions('tse')
    show = len(list(request.args.values())) > 0
    mode = request.args.get('mode', "athenas")

    return render_template(
        "tse2.html",
        options=options,
        page=2,
        show=show,
        mode=mode,
        years=[2018, 2016, 2014, 2012, 2010, 2008, 2006, 2004, 2002, 2000, 1998],
        uf_list=get_uf_list(),
        mun_list=get_mun_list(),
        lang=get_locale()
    )


def consulta_tse():
    session['back'] = request.path
    options = AthenaQueryOptions('tse')
    show = len(list(request.args.values())) > 0
    mode = request.args.get('mode', "athenas")

    return render_template(
        "tse.html",
        options=options,
        page=2,
        show=show,
        mode=mode,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        mun_list=get_mun_list(),
        lang=get_locale()
    )


def consulta_candidatos():
    session['back'] = request.path
    options = AthenaQueryOptions('candidatos')
    show = len(list(request.args.values())) > 0
    mode = request.args.get('mode', "athenas")

    return render_template(
        "candidatos.html",
        options=options,
        page=3,
        show=show,
        mode=mode,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        lang=get_locale()
    )


def consulta_legendas():
    session['back'] = request.path
    options = AthenaQueryOptions('legendas')
    show = len(list(request.args.values())) > 0
    mode = request.args.get('mode', "athenas")

    return render_template(
        "legendas.html",
        options=options,
        page=4,
        show=show,
        mode=mode,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        lang=get_locale()
    )


def consulta_votos():
    session['back'] = request.path
    options = AthenaQueryOptions('votos')
    show = len(list(request.args.values())) > 0
    mode = request.args.get('mode', "athenas")

    return render_template(
        "votos.html",
        options=options,
        page=5,
        show=show,
        mode=mode,
        years=get_years(options.job),
        uf_list=get_uf_list(),
        lang=get_locale()
    )


def consulta_bem_candidato():
    session['back'] = request.path
    options = AthenaQueryOptions('bem_candidato')
    show = len(list(request.args.values())) > 0
    mode = request.args.get('mode', "athenas")

    return render_template(
        "bem_candidato.html",
        options=options,
        page=6,
        show=show,
        mode=mode,
        years=[2018, 2016, 2014, 2012, 2010, 2008, 2006],
        uf_list=get_uf_list(),
        lang=get_locale()
    )


def consulta_filiados():
    session['back'] = request.path
    options = AthenaQueryOptions('filiados')
    show = len(list(request.args.values())) > 0
    mode = request.args.get('mode', "athenas")

    return render_template(
        "filiados.html",
        options=options,
        page=7,
        show=show,
        mode=mode,
        parties=["avante", "dc", "dem", "mdb", "novo", "patri", "pc_do_b", "pcb", "pco", "pdt", "phs", "pmb", "pmn",
                 "pode", "pp", "ppl", "pps", "pr", "prb", "pros", "prp", "prtb", "psb", "psc", "psd", "psdb", "psl",
                 "psol", "pstu", "pt", "ptb", "ptc", "pv", "rede", "solidariedade"],
        uf_list=get_uf_list(),
        lang=get_locale()
    )


def consulta_secretarios():
    session['back'] = request.path
    options = AthenaQueryOptions('secretarios')
    show = len(list(request.args.values())) > 0
    mode = request.args.get('mode', "athenas")

    return render_template(
        "secretarios.html",
        options=options,
        page=8,
        show=show,
        mode=mode,
        names_list=get_nomes_secretarios_list(),
        uf_list=get_uf_list(),
        periods=["1998-2002", "2002-2006", "2006-2010", "2010-2014", "2014-2018"],
        lang=get_locale()
    )
