import logging
from datetime import datetime
from traceback import format_exc
from typing import NoReturn, Optional

from flask import Flask, request
from pydantic import ValidationError

from news_system.api.auth import auth_bp
from news_system.exception import APIError
from news_system.extensions import cors, db
from news_system.utils.network import response_json

logger = logging.getLogger()


def create_app(config_name: Optional[str] = None) -> Flask:
    """
    加载基本配置
    :return:
    """
    app = Flask('new_system')
    app.config.from_pyfile('news_system/settings.py')
    register_blueprints(app)
    register_errors(app)
    return app


def register_blueprints(app: Flask) -> NoReturn:
    """
    加载蓝本
    :param app:
    :return:
    """
    app.register_blueprint(auth_bp, url_prefix="/oauth")


def register_extensions(app: Flask) -> NoReturn:
    """
    初始化拓展
    :param app:
    :return:
    """
    db.init_app(app)
    cors.init_app(app)


def register_errors(app: Flask) -> NoReturn:
    """
    加载错误页
    :param app:
    :return:
    """

    @app.errorhandler(400)
    def page_not_found(e) -> response_json:
        return response_json(code=400, msg="请求报文存在语法错误"), 400

    @app.errorhandler(404)
    def page_not_found(e) -> response_json:
        return response_json(code=404, msg="找不到此资源"), 404

    @app.errorhandler(405)
    def method_not_allowed(e) -> response_json:
        return response_json(code=405, msg="方法不被允许"), 405

    @app.errorhandler(Exception)
    def the_api_error(e) -> response_json:
        if isinstance(e, APIError):
            return response_json(code=e.code, msg=e.msg, data=e.data)

        if isinstance(e, ValidationError):
            # 处理 pydantic 验证错误
            err_msg = []
            for error in e.errors():
                msg = [' -> '.join(str(e) for e in error['loc']), error["msg"]]
                err_msg.append(', '.join(msg))

            return response_json(code=422, msg="; ".join(err_msg))

        with open("err.log", "a") as f:
            f.write(f"\n{request.url} - {request.remote_addr} - {request.method}\n")
            f.write(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
            f.write(f"\n{format_exc()}")
            f.write("\n")

        logger.exception(e)
        return response_json(code=500, msg="服务器内部错误"), 500
