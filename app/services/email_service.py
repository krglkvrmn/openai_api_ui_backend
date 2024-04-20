from pathlib import Path
from urllib.parse import urlencode

from sendgrid import Mail, SendGridAPIClient

from app.core.settings import settings


def send_verification_email(token: str, email: str):
    verifiication_link = settings.MAIN_PAGE_URL.unicode_string() + 'verification?' + urlencode({'vt': token})
    if not settings.SEND_EMAILS:
        print(verifiication_link)
        return
    email_html_path = settings.APP_ROOT / 'templates' / 'verification_email.html'
    message = Mail(
        from_email='verification@chat.krglkvrmn.me',
        to_emails=email,
        subject='Verify Your Email Address',
        html_content=email_html_path.read_text().format(verification_link=verifiication_link)
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY.get_secret_value())
    sg.send(message)


def send_forgot_password_email(token: str, email: str):
    reset_password_link = settings.MAIN_PAGE_URL.unicode_string() + 'forgot-password?' + urlencode({'prt': token})
    if not settings.SEND_EMAILS:
        print(reset_password_link)
        return

    email_html_path = settings.APP_ROOT / 'templates' / 'password_reset_email.html'
    message = Mail(
        from_email='reset-password@chat.krglkvrmn.me',
        to_emails=email,
        subject='Reset your password',
        html_content=email_html_path.read_text().format(reset_password_link=reset_password_link)
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY.get_secret_value())
    sg.send(message)