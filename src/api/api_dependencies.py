from datetime import datetime

from fastapi import Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates


from typing import Annotated

from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from src.api.exceptions import (
    TokenExpiredException,
    UserIsNotPresentException,
)
from src.crud.user import UserCRUD
from src.db.session import get_db_session
from src.models import User

db_dependency = Annotated[AsyncSession, Depends(get_db_session)]
templates = Jinja2Templates(directory="src/templates")


def get_token(request: Request):
    token_cookies = request.session.get("token")
    if token_cookies:
        return token_cookies

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please, log in or register first",
    )


async def get_current_user(
    token: str = Depends(get_token),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        return None

    # Check token expiration
    expire = payload.get("exp")
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException()

    # Check if the token and user match
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException()

    # Check if user is present in database
    user = await UserCRUD(session).select_one_or_none_filter_by(id=int(user_id))
    if not user:
        raise UserIsNotPresentException()

    return user
