from flask import Flask
from flask_babel import Babel

from web.cepesp.config import APP_SECRET_KEY, APP_DEBUG, BUGSNAG_API_KEY, FLASK_ENV
from web.cepesp.routes import lang
from web.cepesp.routes.api import athena_query_api, athena_status_api, athena_result_api, athena_api, columns_api
from web.cepesp.routes.error import handle_error
from web.cepesp.routes.filters import asset_filter
from web.cepesp.routes.lang import lang
from web.cepesp.routes.queries import consulta_tse, consulta_candidatos, consulta_legendas, consulta_votos, \
    consulta_bem_candidato, consulta_filiados, consulta_secretarios, consulta_tse_2
from web.cepesp.routes.sql import sql
from web.cepesp.routes.static import home, about, others, about_state_secretaries, static_from_root, documentation, \
    spatial2_docs
from web.cepesp.utils.session import get_locale

application = Flask(__name__)
application.env = FLASK_ENV
application.secret_key = APP_SECRET_KEY
application.testing = APP_DEBUG

if BUGSNAG_API_KEY:
    import bugsnag
    import bugsnag.flask

    bugsnag.configure(
        api_key=BUGSNAG_API_KEY,
        project_root="/web",
        release_stage=FLASK_ENV
    )
    bugsnag.flask.handle_exceptions(application)

babel = Babel(application)
babel.localeselector(get_locale)
application.register_error_handler(Exception, handle_error)
application.add_template_filter(lambda fl: asset_filter(fl, application.root_path), "asset")

application.add_url_rule("/", "home", home)
application.add_url_rule("/sobre", "about", about)
application.add_url_rule("/others", "others", others)
application.add_url_rule("/about-state-secretaries", "about_state_secretaries", about_state_secretaries)
application.add_url_rule("/documentacao", "documentation", documentation)
application.add_url_rule("/docs/cepesp-data", "docs_cepesp_data", documentation)
application.add_url_rule("/docs/spatial2", "docs_spatial2", spatial2_docs)

application.add_url_rule("/api/consulta/tse", "api_tse", lambda: athena_api("tse"))
application.add_url_rule("/api/consulta/candidatos", "api_candidatos", lambda: athena_api("candidatos"))
application.add_url_rule("/api/consulta/legendas", "api_legendas", lambda: athena_api("legendas"))
application.add_url_rule("/api/consulta/votos", "api_votos", lambda: athena_api("votos"))
application.add_url_rule("/api/consulta/bem_candidato", "api_bem_candidato", lambda: athena_api("bem_candidato"))
application.add_url_rule("/api/consulta/filiados", "api_filiados", lambda: athena_api("filiados"))
application.add_url_rule("/api/consulta/secretarios", "api_secretarios", lambda: athena_api("secretarios"))

application.add_url_rule("/api/consulta/athena/columns", "athena_columns_api", columns_api)
application.add_url_rule("/api/consulta/athena/query", "athena_query_api", athena_query_api)
application.add_url_rule("/api/consulta/athena/status", "athena_status_api", athena_status_api)
application.add_url_rule("/api/consulta/athena/result", "athena_result_api", athena_result_api)

application.add_url_rule("/consulta/tse", "query_tse", consulta_tse)
application.add_url_rule("/consulta/tse2", "query_tse_2", consulta_tse_2)
application.add_url_rule("/consulta/candidatos", "query_candidatos", consulta_candidatos)
application.add_url_rule("/consulta/legendas", "query_legendas", consulta_legendas)
application.add_url_rule("/consulta/votos", "query_votos", consulta_votos)
application.add_url_rule("/consulta/bem_candidato", "query_bem_candidato", consulta_bem_candidato)
application.add_url_rule("/consulta/filiados", "query_filiados", consulta_filiados)
application.add_url_rule("/consulta/secretarios", "query_secretarios", consulta_secretarios)

application.add_url_rule("/consulta/sql", "sql", sql)

application.add_url_rule("/pt", "lang_pt", lambda: lang("pt"))
application.add_url_rule("/en", "lang_en", lambda: lang("en"))

# SEO
application.add_url_rule("/robots.txt", "robots_txt", static_from_root)
application.add_url_rule("/sitemap.xml", "sitemap_xml", static_from_root)


if __name__ == "__main__":
    application.debug = APP_DEBUG
    application.run()
