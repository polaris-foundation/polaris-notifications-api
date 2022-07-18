from environs import Env
from requests import Response, post


def send_email(email_type: str, email_address: str) -> Response:
    base_url: str = Env().str(
        "DHOS_NOTIFICATIONS_BASE_URL", "http://dhos-notifications-api:5000"
    )

    return post(
        f"{base_url}/dhos/v1/email",
        json={
            "email_type": email_type,
            "email_address": email_address,
        },
    )
