import os
from flask import Flask
from json import JSONEncoder
from datetime import date
from flask import Flask
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    from api.controllers import bp
    app.register_blueprint(bp)

    return app

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return super().default(o)
