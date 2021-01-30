import time

from flask import jsonify


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
    return jsonify(data=data, code=code, msg=msg, now_ts=int(time.time()))
