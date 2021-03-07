from enum import IntEnum, unique
from typing import Optional

from flask import Blueprint, request
from flask.views import MethodView
from pydantic import BaseModel, Field

from news_system.extensions import db
from news_system.model.comments import Comments
from news_system.model.news import News
from news_system.model.tags import Tags
from news_system.utils.network import response_json

news_bp = Blueprint("news", __name__)


@unique
class SizeEnum(IntEnum):
    """ 枚举Size """
    ten = 10
    twenty = 20
    fifty = 50


class FilterGetModel(BaseModel):
    """ 查询标签列表的参数校验 """
    page: Optional[int] = Field(1)
    size: Optional[SizeEnum] = Field(20)
    filter: Optional[str] = Field(min_length=1, max_length=16)


class TagsPostModel(BaseModel):
    """ 新增标签的参数校验 """
    tag: str = Field(min_length=1, max_length=16)


# noinspection DuplicatedCode
class TagsAPI(MethodView):
    # noinspection PyUnresolvedReferences
    @staticmethod
    def get() -> response_json:
        query = FilterGetModel(**request.args)
        tags_query = Tags.query.filter_by(status=0)
        if query.filter is not None:
            tags_query = tags_query.filter(Tags.tag.like(f'%{query.filter}%'))

        tags = tags_query.order_by(db.text('-update_time')).paginate(page=query.page, per_page=query.size)  # 按条件查询tag
        items = [tag.to_dict() for tag in tags.items]  # 列表生成器

        return response_json(data={
            'items': items,
            'page': tags.page,
            'size': tags.per_page,
            'pages': tags.pages,
            'total': tags.total,
            'has_more': tags.has_next,
        })

    @staticmethod
    def post() -> response_json:
        body = TagsPostModel(**request.get_json())
        tag = Tags(tag=body.tag)
        db.session.add(tag)
        db.session.commit()
        return response_json(msg=f"{body.tag} 创建成功")


class NewsModel(BaseModel):
    """ 新增新闻的参数校验 """
    title: str = Field(max_length=255)
    content: str
    tag_id: int = Field(ge=0)


# noinspection DuplicatedCode
class NewsAPI(MethodView):

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get() -> response_json:
        query = FilterGetModel(**request.args)
        news_query = News.query.filter_by(status=0)
        if query.filter is not None:
            news_query = news_query.filter(News.tag.like(f'%{query.filter}%'))

        news = news_query.paginate(page=query.page, per_page=query.size)
        items = [new.to_dict(level="tag") for new in news.items]  # 列表生成器

        return response_json(data={
            'items': items,
            'page': news.page,
            'size': news.per_page,
            'pages': news.pages,
            'total': news.total
        })

    @staticmethod
    def post() -> response_json:
        body = NewsModel(**request.get_json())
        new = News(**body.dict())
        db.session.add(new)
        db.session.commit()
        return response_json(msg=f"{body.title} 创建成功")


class NewAPI(MethodView):
    # noinspection PyUnresolvedReferences
    @staticmethod
    def put(news_id: int) -> response_json:
        body = NewsModel(**request.get_json())
        new = News.query.filter_by(id=news_id, status=0).first()
        if new is None:
            return response_json(code=400, msg="该新闻不存在")

        new.title = body.title
        new.content = body.content
        new.tag_id = body.tag_id
        db.session.add(new)
        db.session.commit()
        return response_json(msg=f"{body.title} 修改成功")


class CommentPostModel(BaseModel):
    comment: str = Field(max_length=255)


class CommentsAPI(MethodView):
    # noinspection PyUnresolvedReferences
    @staticmethod
    def get(news_id: int) -> response_json:
        query = FilterGetModel(**request.args)
        comments = Comments.query.filter_by(news_id=news_id, status=0).paginate(page=query.page, per_page=query.size)
        items = [comment.to_dict() for comment in comments.items]  # 列表生成器
        return response_json(data={
            'items': items,
            'page': comments.page,
            'size': comments.per_page,
            'pages': comments.pages,
            'total': comments.total
        })

    @staticmethod
    def post(news_id: int) -> response_json:
        body = CommentPostModel(**request.get_json())
        comment = Comments(comment=body.comment, news_id=news_id)
        db.session.add(comment)
        db.session.commit()
        return response_json(msg=f"评论成功")


news_bp.add_url_rule(rule="", view_func=NewsAPI.as_view("news"), methods=("GET", "POST"))
news_bp.add_url_rule(rule="/<int:news_id>", view_func=NewAPI.as_view("new"), methods=("PUT",))
news_bp.add_url_rule(rule="/<int:news_id>/comments", view_func=CommentsAPI.as_view("comments"), methods=("GET", "POST"))
news_bp.add_url_rule(rule="/tags", view_func=TagsAPI.as_view("tags"), methods=("GET", "POST"))
