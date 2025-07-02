import os
from email.message import EmailMessage
import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


async def send_email(to_email: str, subject: str, content: str):
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    await aiosmtplib.send(
        message,
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_USER,
        password=EMAIL_PASSWORD,
        use_tls=True,
    )
