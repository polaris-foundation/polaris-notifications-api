from typing import Optional

import requests
from environs import Env
from requests import Response


def _get_base_url() -> str:
    base_url: str = Env().str("FAKE_SMTP_BASE_URL", "http://fake-smtp:1080")
    return f"{base_url}/api/emails"


def get_messages(
    message_from: Optional[str] = None, message_to: Optional[str] = None
) -> Response:
    params: dict = {
        "from": message_from,
        "to": message_to,
    }
    return requests.get(_get_base_url(), timeout=15, params=params)


def delete_messages() -> Response:
    return requests.delete(
        _get_base_url(),
        timeout=15,
    )
