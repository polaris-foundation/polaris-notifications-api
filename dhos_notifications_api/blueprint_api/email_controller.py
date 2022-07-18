from auth0_api_client import mgmt as auth0_mgmt
from auth0_api_client.errors import Auth0ConnectionError
from flask import current_app
from flask_batteries_included.helpers.error_handler import ServiceUnavailableException

from dhos_notifications_api.blueprint_api import email


def send_welcome_email(email_address: str) -> None:
    subject: str = "You have been invited to use a Sensyne Health product."
    send_email(email_address=email_address, subject=subject)


def send_email(email_address: str, subject: str) -> None:

    smtp_host = current_app.config["SMTP_HOST"]
    smtp_auth_user = current_app.config["SMTP_AUTH_USER"]
    smtp_auth_pass = current_app.config["SMTP_AUTH_PASS"]
    email_sender = current_app.config["EMAIL_SENDER"]

    # request a password change ticket in auth0
    try:
        ticket_url = auth0_mgmt.request_password_reset(str(email_address))
    except Auth0ConnectionError:
        raise ServiceUnavailableException("Could not update user's password in Auth0")

    # load mail template and format with ticket url
    mail_body = email.template(ticket_url)

    # send the email to the clinician
    email.send(
        smtp_auth_user,
        smtp_auth_pass,
        smtp_host,
        email_sender,
        email_address,
        subject,
        mail_body,
    )
