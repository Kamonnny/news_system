from functools import wraps

from news_system.utils.token import get_user_by_token


def require_auth(func):
    """ 限制登录才能访问 """

    @wraps(func)
    def wrapper(*args, **kw):
        get_user_by_token()
        return func(*args, **kw)

    return wrapper
