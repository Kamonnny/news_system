from os import getenv

from flask import Flask
from flask_cors import CORS
from news_system.extensions import db

from news_system.api.auth import auth_bp


def create_app(config_name=None) -> Flask:
    """
    加载基本配置
    :return:
    """
    app = Flask('new_system')
    CORS(app)
    app.config.from_pyfile('settings.py')
    register_blueprints(app)
    return app


def register_blueprints(app) -> None:
    """
    加载蓝本
    :param app:
    :return:
    """
    app.register_blueprint(auth_bp, url_prefix="/oauth")


def register_extensions(app) -> None:
    """
    初始化拓展
    :param app:
    :return:
    """
    db.init_app(app)
