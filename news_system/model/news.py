from datetime import datetime

from news_system.extensions import db
from news_system.model.tags import Tags


# noinspection PyUnresolvedReferences
class News(db.Model):
    """新闻表"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    tag_id = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self, level="default"):
        data = {
            "news_id": self.id,
            "title": self.title,
            "content": self.content,
            "tag_id": self.tag_id,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }

        if level == "tag":
            tag = Tags.query.filter_by(id=self.tag_id).first()
            data["tag"] = tag.to_dict() if tag else None

        return data
