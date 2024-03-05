import os
import smtplib
from email.message import EmailMessage

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

from src.api.utils import db_dependency
from src.crud.user import UserCRUD

load_dotenv(".env")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery.conf.beat_schedule = {
    'send_daily_report': {
        'task': 'celery_worker.send_daily_report',
        'schedule': crontab(hour="18", minute="0"),
    },
}


def get_email_template_dashboard(user_email: str):
    """Email template"""
    email = EmailMessage()
    email['Subject'] = 'Daily email'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello. This is your daily notification</h1>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
async def send_email_report(session: db_dependency):
    """Task for sending daily reports to all users"""
    emails = await UserCRUD(session).select_all_emails()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        for email in emails:
            email_msg = get_email_template_dashboard(email)
            server.send_message(email_msg)