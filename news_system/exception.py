class APIError(Exception):
    def __init__(self, code: int = 200, msg: str = "ok", data: dict = None):
        self.code = code
        self.msg = msg
        self.data = data or {}
