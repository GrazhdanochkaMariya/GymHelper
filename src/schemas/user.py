from datetime import datetime
from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError
import phonenumbers

from pydantic import BaseModel, field_validator

email_example = {"email": "user@gmail.com"}
phone_number_example = {"phone_number": "user@gmail.com"}


class UserEmail(BaseModel):
    """Schema to validate email"""

    email: str

    @field_validator("email")
    def email_validator(cls, v):
        try:
            validate_email(v, check_deliverability=False)
            return v
        except EmailNotValidError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email format",
            )

    model_config = {"json_schema_extra": {"examples": [email_example]}}


class UserPhoneNumber(BaseModel):
    """Schema to validate phone number"""

    phone_number: str

    @field_validator("phone_number")
    def validate_phone_number(cls, v: str):
        try:
            phone_number = phonenumbers.parse(v, None)
            return phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.phonenumberutil.NumberParseException:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid phone number format",
            )

    model_config = {"json_schema_extra": {"examples": [phone_number_example]}}


class UserCreate(UserEmail, UserPhoneNumber):
    """Schema to create user"""

    hashed_password: str

    model_config: dict = {"from_attributes": True}


class UserGet(UserEmail, UserPhoneNumber):
    """Schema to get user"""

    id: int
    created_at: datetime

    model_config: dict = {"from_attributes": True}
