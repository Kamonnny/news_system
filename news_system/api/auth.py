from flask import Blueprint, request
from flask.views import MethodView
from pydantic import BaseModel, Field, EmailStr

from news_system.utils.network import response_json

auth_bp = Blueprint("auth", __name__)


class OauthPostModel(BaseModel):
    user_name: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=6)


class OauthAPI(MethodView):

    @staticmethod
    def post() -> response_json:
        body = OauthPostModel(**request.get_json())
        print(body.dict())
        return response_json()


# 注册
class RegisterPostModel(BaseModel):
    user_name: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=6)
    email: EmailStr


class Register(MethodView):

    @staticmethod
    def post() -> response_json:
        body = RegisterPostModel(**request.get_json())
        print(body.dict())
        return response_json()


auth_bp.add_url_rule(rule="", view_func=OauthAPI.as_view("oauth"), methods=("POST",))
auth_bp.add_url_rule(rule="/register", view_func=Register.as_view("oauth"), methods=("POST",))
