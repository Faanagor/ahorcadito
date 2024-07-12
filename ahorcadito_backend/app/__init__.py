from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def create_app():
    app = Flask(__name__)

    from .routes import api_bp

    app.register_blueprint(api_bp)

    return app
