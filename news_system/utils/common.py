from hashlib import md5


def upper_md5(s: str) -> str:
    """
    封装全大写 md5
    :param s:
    :return:
    """
    if not isinstance(s, bytes): s = bytes(s, encoding='utf-8')
    return md5(s).hexdigest().upper()
