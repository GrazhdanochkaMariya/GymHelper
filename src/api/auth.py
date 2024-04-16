from fastapi import APIRouter, Request, HTTPException, status

from src.api.api_dependencies import db_dependency
from src.api.utils import (
    responses,
    verify_password,
    validation_handler,
    get_password_hash,
    create_access_token,
)
from src.crud.user import UserCRUD
from src.schemas.user import UserGet, UserCreate

router = APIRouter(tags=["Authentication"])

# TODO Add profile photo


@router.post(
    "/login",
    response_model=UserGet,
    responses=responses,
    summary="Sign in a user",
)
async def login_user(
    request: Request,
    email: str,
    password: str,
    session: db_dependency,
):
    """Sign in a user"""

    user = await UserCRUD(session).select_one_or_none_filter_by(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User does not exist",
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid password"
        )
    access_token = create_access_token({"sub": str(user.id)})
    request.session.update({"token": access_token})

    return user


@router.post(
    "/signup",
    responses=responses,
    response_model=UserGet,
    summary="Create User",
)
async def signup_user(
    request: Request,
    session: db_dependency,
    password: str,
    phone_number: str,
    email: str,
    name: str,
    age: int,
    last_name: str,
):
    """Create User"""
    data = {
        "phone_number": phone_number,
        "email": email,
        "name": name,
        "last_name": last_name,
        "age": age,
        "hashed_password": get_password_hash(password),
    }
    await validation_handler(pydantic_model=UserCreate, data=data)

    exist_user = await UserCRUD(session).select_all_filter_by(email=email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A user with this email already exists",
        )

    user = await UserCRUD(session).create(**data)
    access_token = create_access_token({"sub": str(user.id)})
    request.session.update({"token": access_token})

    return user


@router.post(
    "/logout",
    responses=responses,
    summary="Log out User",
)
async def logout_user(
    request: Request,
):
    """Log out from User account"""
    request.session.clear()

    return True
