from functools import wraps

from flask import request

from news_system.exception import APIError
from news_system.utils.token import get_user_by_token


def require_auth(func):
    """ 限制登录才能访问 """

    @wraps(func)
    def wrapper(*args, **kw):
        get_user_by_token()
        return func(*args, **kw)

    return wrapper


def require_sudo(func):
    """ 限制超级管理员才能访问 """

    @wraps(func)
    def wrapper(*args, **kw):
        if not request.user.is_admin:
            raise APIError(msg="您没有权限", code=403)
        return func(*args, **kw)

    return wrapper
