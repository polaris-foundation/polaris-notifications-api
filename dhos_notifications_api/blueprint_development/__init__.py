from flask import Blueprint, Response, abort, current_app

development_blueprint = Blueprint("dhos/dev", __name__)


@development_blueprint.route("/reset_test_data")
def reset_test_data() -> Response:
    abort(501)


@development_blueprint.route("/drop_data", methods=["POST"])
def drop_data_route() -> Response:
    if current_app.config["ALLOW_DROP_DATA"] is not True:
        raise PermissionError("Cannot drop data in this environment")
    abort(501)
