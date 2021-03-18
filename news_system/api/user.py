from flask import Blueprint, request

from news_system.utils.network import response_json
from news_system.utils.decorators import require_auth

users_bp = Blueprint("users", __name__)


@users_bp.route("", methods=("GET",))
@require_auth
def get_users():
    return response_json(data=request.user.to_dict())
