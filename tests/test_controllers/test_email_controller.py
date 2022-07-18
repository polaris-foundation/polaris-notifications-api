from _pytest.monkeypatch import MonkeyPatch
from auth0_api_client import mgmt as auth0_mgmt
from flask import Flask
from mock import Mock
from pytest_mock import MockFixture

from dhos_notifications_api.blueprint_api import email_controller


class TestEmailController:
    def test_send_welcome_email(
        self,
        app: Flask,
        mocker: MockFixture,
        monkeypatch: MonkeyPatch,
    ) -> None:

        monkeypatch.setitem(app.config, "DISABLE_EMAIL_SEND", True)

        ticket_url = "dummy"

        mock_method: Mock = mocker.patch.object(
            auth0_mgmt, "request_password_reset", return_value=ticket_url
        )

        email_controller.send_welcome_email(email_address="dave.roberts@mail.com")

        mock_method.call_count == 1
