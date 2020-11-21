from flask import Blueprint
from flask.views import MethodView

from news_system.utils.network import response_json, get_request_body

auth_bp = Blueprint("auth", __name__)


class OauthAPI(MethodView):

    @staticmethod
    def post() -> response_json:
        """
        登录接口
        :return:
        """

        return response_json()


auth_bp.add_url_rule(rule="", view_func=OauthAPI.as_view("oauth"), methods=("POST",))
