import os
from flask import Flask
from .model import configure as configure_db
from .serealizer import configure as configure_ma
from .UsuarioBluePrint import bp_usuarios


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/oa_api'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    configure_db(app)
    configure_ma(app)

    app.register_blueprint(bp_usuarios)
    return app
