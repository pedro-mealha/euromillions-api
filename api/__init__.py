import os
from flask import Flask
from flask_cors import CORS
from json import JSONEncoder
from datetime import date
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

def create_app() -> Flask:
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config["CORS_METHODS"] = ["GET", "OPTIONS"]
    CORS(app)

    from api.controllers import bp
    app.register_blueprint(bp)

    return app

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return super().default(o)
