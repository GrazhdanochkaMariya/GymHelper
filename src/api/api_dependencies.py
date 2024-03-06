from datetime import datetime

from fastapi import Depends

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from config import settings
from src.api.exceptions import (
    IncorrectTokenException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from src.api.utils import get_token
from src.db.session import get_db_session
from src.models import User


db_dependency = Annotated[AsyncSession, Depends(get_db_session)]


async def get_current_user(
    token: str = Depends(get_token),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenException()

    # Check token expiration
    expire = payload.get("exp")
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException()

    # Check if the token and user match
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException()

    # Check if user is present in database
    user = await User(session).select_one_or_none_filter_by(id=int(user_id))
    if not user:
        raise UserIsNotPresentException()

    return user
