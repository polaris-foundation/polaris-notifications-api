import os
import smtplib
from email.mime.text import MIMEText

from flask import current_app
from she_logging import logger


def template(ticket: str) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    with open(f"{here}/../templates/mail-body.html", "r") as f:
        mail_body_raw = f.read()
    return mail_body_raw.replace("{{ url }}", ticket)


def send(
    username: str,
    password: str,
    server: str,
    sender: str,
    recipient: str,
    subject: str,
    body: str,
) -> None:

    if current_app.config["DISABLE_EMAIL_SEND"]:
        return

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    smtp = smtplib.SMTP(server, 587)
    smtp.ehlo()
    smtp.starttls(keyfile=None, certfile=None, context=None)
    smtp.login(username, password)
    logger.debug("Sending email to %s", recipient)
    smtp.sendmail(
        from_addr=sender,
        to_addrs=[recipient],
        msg=msg.as_string(),
        mail_options=[],
        rcpt_options=[],
    )
    smtp.quit()
