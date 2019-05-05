from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config

bootstrap = Bootstrap()
db = SQLAlchemy()
config = Config()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    config.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app