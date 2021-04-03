import os
from flask import Flask

from flask import Flask
from dotenv import load_dotenv

from api.utils.db import Database

APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

db = Database()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.getenv('SECRET_KEY') or 'dev_key'
    )

    from api.controllers import bp
    app.register_blueprint(bp)

    return app
