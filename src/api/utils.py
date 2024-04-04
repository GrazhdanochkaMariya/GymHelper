import os
import smtplib
from datetime import timedelta, datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, List
from pydantic import ValidationError
from passlib.context import CryptContext
from jose import jwt
import matplotlib.pyplot as plt


from fastapi import status, HTTPException

from config import settings
from src.models import UserMeasurements
from src.schemas.base import MessageResponse

responses = {
    status.HTTP_200_OK: {"model": MessageResponse},
    status.HTTP_400_BAD_REQUEST: {"model": MessageResponse},
    status.HTTP_401_UNAUTHORIZED: {"model": MessageResponse},
    status.HTTP_404_NOT_FOUND: {"model": MessageResponse},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": MessageResponse},
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def validation_handler(pydantic_model, data):
    try:
        pydantic_model(**data)
    except ValidationError as e:
        error_msg = "Validation error"
        if e.errors():
            error_msg = e.errors()[0]["msg"]
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error_msg
        )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_email_template_measurements(user_email: str):
    """Email template"""
    email = MIMEMultipart()
    email["Subject"] = "Email with measurements"
    email["From"] = settings.SMTP_USER
    email["To"] = user_email

    text_part = MIMEText(
        "<h1 style='color: red;'>Dear user, here are your measurements</h1>", "html"
    )
    email.attach(text_part)

    return email


def send_single_email(email: str, attachment=None):
    """Send single email with attachment"""
    email_msg = get_email_template_measurements(email)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"user_measurements_{timestamp}"

    if attachment:
        attachment_part = MIMEApplication(
            attachment.getvalue(), Name="measurements.xlsx"
        )
        attachment_part["Content-Disposition"] = f"attachment; filename={filename}.xlsx"
        email_msg.attach(attachment_part)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email_msg)


def create_dynamics_plot(user_measurements: List[UserMeasurements], plots_dir: str):
    weights = [measurement.weight for measurement in user_measurements]
    dates = [
        measurement.created_at.strftime("%Y-%m-%d %H:%M")
        for measurement in user_measurements
    ]

    user_id = user_measurements[0].user_id
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plot_name = f"measurements_plot_{user_id}_{timestamp}"

    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker="o", color="blue", linestyle="-")
    plt.title("Weight Dynamics")
    plt.xlabel("Date")
    plt.ylabel("Weight")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plot_path = os.path.join(plots_dir, f"{plot_name}.png")
    plt.savefig(plot_path)
    plt.close()

    return plot_path
