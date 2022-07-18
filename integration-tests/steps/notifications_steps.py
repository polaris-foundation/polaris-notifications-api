import json

from behave import step
from behave.runner import Context
from clients.fake_smtp_server_client import get_messages
from clients.notifications_client import send_email
from environs import Env
from faker import Faker
from requests import Response, codes


@step("there exists a user")
def get_random_user_body(context: Context, email_kind: str = None) -> None:
    context.recipient = Faker().email()


@step("a {email_type} is sent to the user")
def send_notification(context: Context, email_type: str = None) -> None:
    send_email(email_type=email_type, email_address=context.recipient)


@step("the user {receives_or_not} the email")
def assert_email_received(context: Context, receives_or_not: str) -> None:
    message_from = Env().str("EMAIL_SENDER")
    response: Response = get_messages(message_from, message_to=context.recipient)
    response.raise_for_status()
    messages: list = response.json()

    if receives_or_not == "receives":
        assert 1 == len(messages)
    elif receives_or_not == "does not receive":
        assert 0 == len(messages)
    else:
        raise ValueError(f"Unable to handle {receives_or_not}")
