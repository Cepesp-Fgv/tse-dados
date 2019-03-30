from flask import Flask
from flask_babel import Babel

from web.cepesp.config import APP_SECRET_KEY, APP_DEBUG
from web.cepesp.routes import lang
from web.cepesp.routes.api import votos_api, legendas_api, candidatos_api, bem_candidato_api, tse_api, \
    athena_query_api, athena_status_api, athena_result_api
from web.cepesp.routes.error import handle_error
from web.cepesp.routes.filters import asset_filter
from web.cepesp.routes.lang import lang
from web.cepesp.routes.queries import consulta_tse, consulta_candidatos, consulta_legendas, consulta_votos, \
    consulta_bem_candidato
from web.cepesp.routes.sql import sql
from web.cepesp.routes.static import home, about
from web.cepesp.utils.session import get_locale

application = Flask(__name__)
application.secret_key = APP_SECRET_KEY
application.testing = APP_DEBUG
babel = Babel(application)

babel.localeselector(get_locale)
application.register_error_handler(Exception, handle_error)
application.add_template_filter(lambda fl: asset_filter(fl, application.root_path), 'asset')

application.add_url_rule('/', 'home', home)
application.add_url_rule('/sobre', 'about', about)
application.add_url_rule('/lang/<locale>', 'change_lang', lang)

application.add_url_rule('/api/consulta/tse', 'api_tse', tse_api)
application.add_url_rule('/api/consulta/candidatos', 'api_candidatos', candidatos_api)
application.add_url_rule('/api/consulta/legendas', 'api_legendas', legendas_api)
application.add_url_rule('/api/consulta/votos', 'api_votos', votos_api)
application.add_url_rule('/api/consulta/bem_candidato', 'api_bem_candidato', bem_candidato_api)

application.add_url_rule('/api/consulta/athena/query', 'athena_query_api', athena_query_api)
application.add_url_rule('/api/consulta/athena/status', 'athena_status_api', athena_status_api)
application.add_url_rule('/api/consulta/athena/result', 'athena_result_api', athena_result_api)

application.add_url_rule('/consulta/tse', 'query_tse', consulta_tse)
application.add_url_rule('/consulta/candidatos', 'query_candidatos', consulta_candidatos)
application.add_url_rule('/consulta/legendas', 'query_legendas', consulta_legendas)
application.add_url_rule('/consulta/votos', 'query_votos', consulta_votos)
application.add_url_rule('/consulta/bem_candidato', 'query_bem_candidato', consulta_bem_candidato)

application.add_url_rule('/consulta/sql', 'sql', sql)

langs = ["pt", "en"]
for l in langs:
    application.add_url_rule('/%s' % l, 'lang_%s' % l, lambda: lang(l))

if __name__ == "__main__":
    application.debug = APP_DEBUG
    application.run()
