from typing import Annotated
from pydantic import ValidationError
from passlib.context import CryptContext


from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db_session
from src.schemas.base import MessageResponse

responses = {
    status.HTTP_200_OK: {"model": MessageResponse},
    status.HTTP_400_BAD_REQUEST: {"model": MessageResponse},
    status.HTTP_401_UNAUTHORIZED: {"model": MessageResponse},
    status.HTTP_404_NOT_FOUND: {"model": MessageResponse},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": MessageResponse},
}

db_dependency = Annotated[AsyncSession, Depends(get_db_session)]
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