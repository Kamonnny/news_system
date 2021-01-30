from datetime import datetime

from news_system.extensions import db


class Tags(db.Model):
    """标签表"""
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(16))
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "tag_id": self.id,
            "tag": self.tag,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }
