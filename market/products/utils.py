import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


def send_email(receiver: str, message: str) -> None:
    """
    Отправляет пользователю receiver письмо с сообщением message
    :param receiver: Email пользователя
    :param message: Сообщение
    """
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)

        email = MIMEMultipart()
        email["Subject"] = "Импорт продуктов"
        email["From"] = settings.DEFAULT_FROM_EMAIL
        email["To"] = receiver

        text = MIMEText(message)
        email.attach(text)

        server.sendmail(settings.DEFAULT_FROM_EMAIL, receiver, email.as_string())
