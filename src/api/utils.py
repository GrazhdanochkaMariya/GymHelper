from datetime import timedelta, datetime
from typing import Union
from pydantic import ValidationError
from passlib.context import CryptContext
from jose import jwt


from fastapi import status, HTTPException, Request

from config import settings
from src.api.exceptions import TokenAbsentException
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


def get_token(request: Request):
    token_cookies = request.cookies.get("token")
    if token_cookies:
        return token_cookies

    token_headers = request.headers.get("Authorization")
    if token_headers:
        if token_headers.startswith("Bearer "):
            token = token_headers.split(" ")[1]
            return token

    raise TokenAbsentException()

