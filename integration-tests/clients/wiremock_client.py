import requests
from environs import Env


def _get_mappings_url() -> str:
    base_url: str = Env().str("WIREMOCK_BASE_URL", "http://wiremock:8080")
    return f"{base_url}/__admin/mappings"


def setup_mock_auth0_token_endpoint() -> None:
    payload = {
        "request": {"method": "POST", "url": "/oauth/token"},
        "response": {"status": 200, "jsonBody": {"access_token": "TOKEN"}},
    }
    response = requests.post(_get_mappings_url(), json=payload)
    response.raise_for_status()


def setup_mock_auth0_connections_endpoint() -> None:
    # mock /api/v2/connections, taking into account pagination
    payload = {
        "mappings": [
            {
                "request": {
                    "method": "GET",
                    "urlPathPattern": "/api/v2/connections",
                    "queryParameters": {
                        "page": {"matches": "0"},
                        "per_page": {"matches": ".*"},
                    },
                },
                "response": {
                    "headers": {
                        "Content-Type": "application/json",
                    },
                    "status": 200,
                    "jsonBody": [
                        {
                            "name": "localhost-users",
                            "display_name": "Mock Users",
                            "options": {},
                            "id": "con_0000000000000001",
                            "strategy": "auth0",
                            "realms": ["test"],
                            "is_domain_connection": False,
                            "metadata": {},
                        }
                    ],
                },
            },
            {
                "request": {
                    "method": "GET",
                    "urlPathPattern": "/api/v2/connections",
                    "queryParameters": {
                        "page": {"matches": "[1-9][0-9]*"},
                        "per_page": {"matches": ".*"},
                    },
                },
                "response": {
                    "headers": {
                        "Content-Type": "application/json",
                    },
                    "status": 200,
                    "jsonBody": [],
                },
            },
        ]
    }
    response = requests.post(f"{_get_mappings_url()}/import", json=payload)
    response.raise_for_status()


def setup_mock_auth0_password_change_endpoint() -> None:
    payload = {
        "request": {"method": "POST", "url": "/api/v2/tickets/password-change"},
        "response": {"status": 200, "jsonBody": {"ticket": "TICKET"}},
    }
    response = requests.post(_get_mappings_url(), json=payload)
    response.raise_for_status()
