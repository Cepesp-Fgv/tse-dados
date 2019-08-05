import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

APP_DEBUG = os.getenv('APP_DEBUG') == 'True'
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
GA_TRACKING_ID = os.getenv('GA_TRACKING_ID')
APP_ENV = os.getenv('APP_ENV')
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
API_PYTHON_VERSION = os.getenv('API_PYTHON_VERSION')
API_R_VERSION = os.getenv('API_R_VERSION')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_HOST = os.getenv('DB_HOST')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = int(os.getenv('DB_PORT', 3306))
ATHENA_CACHE = os.getenv('ATHENA_CACHE', 'local')
BUGSNAG_API_KEY = os.getenv('BUGSNAG_API_KEY')
