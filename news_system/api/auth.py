from flask import Blueprint, request
from flask.views import MethodView
from pydantic import BaseModel, EmailStr, Field

from news_system.extensions import db
from news_system.model.users import Users
from news_system.utils.network import response_json
from news_system.utils.token import create_token, validate_token

auth_bp = Blueprint("auth", __name__)


class OauthPostModel(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=6)
    check_admin: bool = Field(False)


class OauthPutModel(BaseModel):
    refresh_token: str = Field(min_length=1)


class OauthAPI(MethodView):

    # noinspection PyUnresolvedReferences
    @staticmethod
    def post() -> response_json:
        body = OauthPostModel(**request.get_json())
        user = Users.query.filter_by(username=body.username).first()
        if user is None:
            return response_json(code=404, msg="用户不存在或者密码错误")

        if not user.validate_password(body.password):
            return response_json(code=404, msg="用户不存在或者密码错误")

        if body.check_admin and not user.is_admin:
            return response_json(code=404, msg="用户不存在或者密码错误")

        return response_json(msg="登录成功", data=create_token(user))

    # noinspection PyUnresolvedReferences
    @staticmethod
    def put() -> response_json:
        body = OauthPutModel(**request.get_json())
        user_id = validate_token(body.refresh_token)['id']
        return response_json(msg="登录成功", data=create_token(Users(id=user_id)))


class RegisterPostModel(BaseModel):
    """ 注册 """
    username: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=6)
    email: EmailStr


class Register(MethodView):

    @staticmethod
    def post() -> response_json:
        """ 注册用户 """
        body = RegisterPostModel(**request.get_json())
        user = Users(username=body.username, email=body.email)
        user.set_password(body.password)
        db.session.add(user)
        db.session.commit()
        return response_json(msg="注册成功")


auth_bp.add_url_rule(rule="", view_func=OauthAPI.as_view("oauth"), methods=("POST", "PUT"))
auth_bp.add_url_rule(rule="/register", view_func=Register.as_view("register"), methods=("POST",))
