import os
from flask import Flask

from flask import Flask
from dotenv import load_dotenv

from api.utils.db import Database

db = Database()

def create_api():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.getenv('SECRET_KEY') or 'dev_key'
    )

    from api.controllers import bp
    app.register_blueprint(bp)

    return app
