from environs import Env
from flask import Flask


class Configuration:
    env = Env()
    SMTP_HOST: str = env.str("SMTP_HOST")
    SMTP_AUTH_PASS: str = env.str("SMTP_AUTH_PASS")
    SMTP_AUTH_USER: str = env.str("SMTP_AUTH_USER")
    EMAIL_SENDER: str = env.str("EMAIL_SENDER")
    DISABLE_EMAIL_SEND: bool = env.bool("DISABLE_EMAIL_SEND", default=False)


def init_config(app: Flask) -> None:
    app.config.from_object(Configuration)
