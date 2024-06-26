from flask import Flask, render_template
# from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config
import json

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_key):

    app = Flask(__name__)

    app.config.from_object(config[config_key])
    app.config.from_envvar("APPLICATION_SETTINGS")
    app.config.from_pyfile("config.py")
    app.config.from_file("config.json", load=json.load)

    # app.config.from_mapping(
    #     SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
    #     SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent/'local.sqlite'}", 
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False, 
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f"
    # )

    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app