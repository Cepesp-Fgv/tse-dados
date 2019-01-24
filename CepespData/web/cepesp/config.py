import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

APP_DEBUG = os.getenv('APP_DEBUG') == 'True'
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
GA_TRACKING_ID = os.getenv('GA_TRACKING_ID')
APP_ENV = os.getenv('APP_ENV')
API_PYTHON_VERSION = os.getenv('API_PYTHON_VERSION')
API_R_VERSION = os.getenv('API_R_VERSION')