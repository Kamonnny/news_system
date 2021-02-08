from enum import IntEnum, unique
from typing import Optional

from flask import Blueprint, request
from flask.views import MethodView
from pydantic import BaseModel, Field

from news_system.extensions import db
from news_system.model.tags import Tags
from news_system.model.news import News
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
        tags_query = Tags.query
        if query.filter is not None:
            tags_query = tags_query.filter(Tags.tag.like(f'%{query.filter}%'))

        tags = tags_query.paginate(page=query.page, per_page=query.size)  # 按条件查询tag
        items = [tag.to_dict() for tag in tags.items]  # 列表生成器

        return response_json(data={
            'items': items,
            'page': tags.page,
            'size': tags.per_page,
            'pages': tags.pages,
            'total': tags.total
        })

    @staticmethod
    def post() -> response_json:
        body = TagsPostModel(**request.get_json())
        tag = Tags(tag=body.tag)
        db.session.add(tag)
        db.session.commit()
        return response_json(msg=f"{body.tag} 创建成功")


class NewsPostModel(BaseModel):
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
        news_query = News.query
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
        body = NewsPostModel(**request.get_json())
        new = News(**body.dict())
        db.session.add(new)
        db.session.commit()
        return response_json(msg=f"{body.title} 创建成功")


news_bp.add_url_rule(rule="", view_func=NewsAPI.as_view("news"), methods=("GET", "POST"))
news_bp.add_url_rule(rule="/tags", view_func=TagsAPI.as_view("tags"), methods=("GET", "POST"))
