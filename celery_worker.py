import logging
import smtplib
from email.message import EmailMessage
from celery import Celery
from celery.schedules import crontab
from sqlalchemy import select

from config import settings
from src.db.session import sync_session_maker
from src.models import User

logger = logging.getLogger(__name__)
schedule_time = crontab(hour="17", minute="30")

celery = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)
celery.conf.update(include=["celery_worker"])
celery.conf.timezone = "Europe/Minsk"
celery.conf.beat_schedule = {
    "send_email_report": {
        "task": "send_email_report",
        "schedule": schedule_time,
    },
}

# TODO Refactor (divide on different modules)


def get_all_emails_from_db():
    with sync_session_maker() as session:
        query = select(User.email)
        result = session.execute(query)
        return result


def get_email_template_dashboard(user_email: str):
    """Email template"""
    email = EmailMessage()
    email["Subject"] = "Daily email"
    email["From"] = settings.SMTP_USER
    email["To"] = user_email

    email.set_content(
        "<div>"
        f'<h1 style="color: red;">Hello. This is your daily notification</h1>'  # noqa
        "</div>",
        subtype="html",
    )
    return email


@celery.task(name="send_email_report")
def send_email_report():
    """Task for sending daily reports to all users"""
    try:
        emails = get_all_emails_from_db()
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            for email in emails:
                email_msg = get_email_template_dashboard(email)
                server.send_message(email_msg)
        logger.info("Task send_email_report executed")
    except Exception as e:
        logger.error(
            f"An error occurred in task send_email_report: {str(e)}", exc_info=True
        )
