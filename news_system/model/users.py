from datetime import datetime
from typing import NoReturn

from werkzeug.security import check_password_hash, generate_password_hash

from news_system.extensions import db


class Users(db.Model):
    """用户表"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(255))
    email = db.Column(db.String(64))
    status = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def set_password(self, password: str) -> NoReturn:
        """设置密码

        :param password:
        :return:
        """
        self.password = generate_password_hash(password)

    def validate_password(self, password: str) -> bool:
        """验证密码

        :param password: 密码
        :return: 密码是否正确
        """
        return check_password_hash(self.password, password)
