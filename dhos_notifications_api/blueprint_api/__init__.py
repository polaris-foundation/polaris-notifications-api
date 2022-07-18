from typing import Dict

from flask import Blueprint, Response, make_response

from dhos_notifications_api.blueprint_api import email_controller

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/dhos/v1/email", methods=["POST"])
def send_email_to_clinician(email_details: Dict[str, str]) -> Response:
    """
    ---
    post:
      summary: Send email
      description: Send email e.g. to new clinician user
      tags: [email]
      requestBody:
        description: Details containing email address and message type
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EmailSendRequest'
              x-body-name: email_details
      responses:
        '201':
          description: Email created and sent
        default:
          description: >-
            Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    if email_details["email_type"] == "WELCOME_EMAIL":
        email_controller.send_welcome_email(email_details["email_address"])

    return make_response("", 201)
