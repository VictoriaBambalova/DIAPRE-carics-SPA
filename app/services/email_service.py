import smtplib
from email.message import EmailMessage

from flask import current_app


def _bool_config(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def send_password_reset_email(recipient_email, reset_url):
    smtp_host = current_app.config.get("SMTP_HOST")
    smtp_port = int(current_app.config.get("SMTP_PORT", 587))
    smtp_user = current_app.config.get("SMTP_USER")
    smtp_password = current_app.config.get("SMTP_PASSWORD")
    smtp_from = current_app.config.get("SMTP_FROM") or smtp_user
    smtp_use_tls = _bool_config(current_app.config.get("SMTP_USE_TLS"), default=True)

    if not smtp_host or not smtp_user or not smtp_password or not smtp_from:
        raise RuntimeError("SMTP settings are missing.")

    message = EmailMessage()
    message["Subject"] = "DIAPRE password reset"
    message["From"] = smtp_from
    message["To"] = recipient_email
    message.set_content(
        "We received a request to reset your DIAPRE password.\n\n"
        f"Reset link: {reset_url}\n\n"
        "If you did not request this, you can ignore this email."
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as smtp:
        if smtp_use_tls:
            smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(message)
