from news_system.extensions import db


class User(db.Model):
    """用户表"""
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32))
    password = db.Column(db.String(255))
    email = db.Column(db.String(64))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    status = db.Column(db.String(32))