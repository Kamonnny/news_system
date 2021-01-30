class APIError(Exception):
    """ 自定义错误类 """

    def __init__(self, code: int = 400, msg: str = "ok", data: dict = None):
        self.code = code
        self.msg = msg
        self.data = data or {}
