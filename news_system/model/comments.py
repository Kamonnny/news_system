from datetime import datetime

from news_system.extensions import db
from news_system.model.users import Users


class Comments(db.Model):
    """评论表"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    news_id = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # noinspection PyUnresolvedReferences
    def to_dict(self):
        return {
            "comment_id": self.id,
            "user": Users.query.filter_by(id=self.user_id).first(),
            "news_id": self.news_id,
            "comment": self.comment,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }
