from os import getenv

from flask import request
from itsdangerous import BadSignature, TimedJSONWebSignatureSerializer

from news_system.exception import APIError
from news_system.model.users import Users


def get_user_by_token() -> dict:
    """
    从请求头获取token，并验证取得 user_id
    :return: token
    """
    try:
        token_type, token = request.headers["Authorization"].split(None, 1)
    except (KeyError, ValueError):
        raise APIError(msg="请重新登录", code=401)

    if token == "null" or token_type.lower() != "bearer":
        raise APIError(msg="请重新登录", code=401)

    # 到这里就拿到了，从前端传过来的token

    # 验证一下token合法性，并获得token里面的数据
    token = validate_token(token, token_type="ACCESS_TOKEN")

    request.user = Users.query.filter_by(id=token['id']).first()


def create_token(user: Users) -> dict:
    """
    生成令牌
    """

    return {
        "access_token": generate_token({"id": user.id}),
        "refresh_token": generate_token({"id": user.id}, token_type="REFRESH_TOKEN", expires_in=2592000)
    }


def generate_token(data: dict, *, token_type: str = "ACCESS_TOKEN", expires_in: int = 3600) -> str:
    """
    生成令牌
    :param data: 令牌的内容
    :param token_type: 令牌的类型，每一个类型对应不同的密钥
    :param expires_in: 有效时间
    :return: 令牌
    """
    s = TimedJSONWebSignatureSerializer(getenv(token_type), expires_in=expires_in)
    token = s.dumps(data).decode("ascii")
    return token


def validate_token(token: str, token_type: str = "REFRESH_TOKEN") -> dict:
    """
    验证令牌
    :param token: 令牌
    :param token_type: 令牌类型
    """
    s = TimedJSONWebSignatureSerializer(getenv(token_type))
    try:
        data = s.loads(token)
    except BadSignature:
        raise APIError(msg="请重新登录", code=401)
    else:
        return data
