import smtplib
from typing import Dict, List

import pytest
from auth0_api_client import mgmt as auth0_mgmt
from auth0_api_client.errors import Auth0ConnectionError
from mock import Mock
from pytest_mock import MockFixture
from werkzeug import Client


class TestApi:
    @pytest.fixture
    def email_send_body_valid(self) -> Dict:
        return {
            "email_address": "some.email@mail.com",
            "email_type": "WELCOME_EMAIL",
        }

    def test_send_email_to_clinician(
        self,
        client: Client,
        email_send_body_valid: Dict,
        mocker: MockFixture,
    ) -> None:

        url: str = f"/dhos/v1/email"
        ticket_url = "dummy"

        mock_methods: List[Mock] = [
            mocker.patch.object(
                auth0_mgmt, "request_password_reset", return_value=ticket_url
            ),
            mocker.patch.object(smtplib.SMTP, "__init__", return_value=None),
            mocker.patch.object(smtplib.SMTP, "ehlo", return_value=None),
            mocker.patch.object(smtplib.SMTP, "starttls", return_value=None),
            mocker.patch.object(smtplib.SMTP, "login", return_value=None),
            mocker.patch.object(smtplib.SMTP, "sendmail", return_value=None),
            mocker.patch.object(smtplib.SMTP, "quit", return_value=None),
        ]

        response = client.post(
            url,
            json=email_send_body_valid,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 201

        for mock_method in mock_methods:
            assert mock_method.call_count == 1

    @pytest.mark.parametrize(
        "body",
        [
            None,
            {"key": "value"},
            [{}, {}],
            {"email_address": "some.email@mail.com", "email_type": "RANDOM"},
        ],
    )
    def test_send_email_to_clinician_failure(
        self,
        client: Client,
        body: Dict,
        mocker: MockFixture,
    ) -> None:

        url: str = f"/dhos/v1/email"

        response = client.post(
            url,
            json=body,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_send_email_to_clinician_auth0_connect_error(
        self,
        client: Client,
        email_send_body_valid: MockFixture,
        mocker: MockFixture,
    ) -> None:

        url: str = f"/dhos/v1/email"
        ticket_url = "dummy"

        mock_method = mocker.patch.object(
            auth0_mgmt,
            "request_password_reset",
            return_value=ticket_url,
            side_effect=Auth0ConnectionError(),
        )

        response = client.post(
            url, json=email_send_body_valid, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 503
        assert mock_method.call_count == 1
