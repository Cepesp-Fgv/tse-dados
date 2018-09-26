from flask import make_response, render_template, request

from web.cepesp.utils.data import COD_SIT


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


def sql_create():
    response = make_response(render_template(
        "sql/create.html",
        # anos=[1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016]
        anos=[2012]
    ))
    response.headers['Content-Disposition'] = 'attachment; filename=sql.txt'
    response.mimetype = 'text/txt'
    return response