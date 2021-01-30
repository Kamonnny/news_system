from flask import Blueprint, request
from flask.views import MethodView
from pydantic import BaseModel, Field, EmailStr


from news_system.extensions import db
from news_system.model.users import Users
from news_system.utils.network import response_json

auth_bp = Blueprint("auth", __name__)


class OauthPostModel(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=6)


class OauthAPI(MethodView):

    @staticmethod
    def post() -> response_json:
        body = OauthPostModel(**request.get_json())
        # user = Users.query.
        return response_json()


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


auth_bp.add_url_rule(rule="", view_func=OauthAPI.as_view("oauth"), methods=("POST",))
auth_bp.add_url_rule(rule="/register", view_func=Register.as_view("register"), methods=("POST",))
