from flask import request, jsonify

from news_system.api_error import APIError


def get_request_body(*keys) -> list:
    """
    获取请求头的 body 数据
    :param keys:
    :return:
    """
    try:
        value = []
        data = request.get_json()
        for key in keys:
            value.append(data[key])
    except (KeyError, TypeError):
        raise APIError("缺少参数")
    else:
        return value


def response_json(data: dict = None, code: int = 200, msg: str = "ok") -> jsonify:
    """
    统一响应 json
    :param data:
    :param code:
    :param msg:
    :return:
    """
    if data is None:
        data = {}
    return jsonify(data=data, code=code, msg=msg)
