from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_batteries_included.helpers.apispec import (
    FlaskBatteriesPlugin,
    initialise_apispec,
    openapi_schema,
)
from marshmallow import INCLUDE, Schema, fields
from marshmallow.validate import OneOf

dhos_notifications_api_spec: APISpec = APISpec(
    version="1.0.0",
    openapi_version="3.0.3",
    title="DHOS Notifications API",
    info={
        "description": "The DHOS Notifications API is responsible for connecting to external communication channels."
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin(), FlaskBatteriesPlugin()],
)

initialise_apispec(dhos_notifications_api_spec)


@openapi_schema(dhos_notifications_api_spec)
class EmailSendRequest(Schema):
    class Meta:
        title = "Email send request data"
        unknown = INCLUDE
        ordered = True

    email_address = fields.String(
        required=True, description="Email address", example="john.roberts@mail.com"
    )
    email_type = fields.String(
        required=True,
        description="Email type",
        validate=OneOf(["WELCOME_EMAIL"]),
        example="WELCOME_EMAIL",
    )
