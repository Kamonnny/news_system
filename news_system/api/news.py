from enum import IntEnum, unique
from typing import Optional

from flask import Blueprint, request
from flask.views import MethodView
from pydantic import BaseModel, Field

from news_system.extensions import db
from news_system.model.tags import Tags
from news_system.utils.network import response_json

news_bp = Blueprint("news", __name__)


@unique
class SizeEnum(IntEnum):
    """ 枚举Size """
    ten = 10
    twenty = 20
    fifty = 50


class TagsGetModel(BaseModel):
    """ 查询标签列表的参数校验 """
    page: Optional[int] = Field(1)
    size: Optional[SizeEnum] = Field(20)
    filter: Optional[str] = Field(min_length=1, max_length=16)


class TagsPostModel(BaseModel):
    """ 新增标签的参数校验 """
    tag: str = Field(min_length=1, max_length=16)


class TagsAPI(MethodView):
    # noinspection PyUnresolvedReferences
    @staticmethod
    def get() -> response_json:
        query = TagsGetModel(**request.args)
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


news_bp.add_url_rule(rule="tags", view_func=TagsAPI.as_view("tags"), methods=("GET", "POST"))
