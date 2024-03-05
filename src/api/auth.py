from fastapi import APIRouter, Request, HTTPException, status, Query

from src.api.utils import responses, db_dependency, verify_password, validation_handler, get_password_hash
from src.crud.user import UserCRUD
from src.schemas.user import UserGet, UserCreate

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login",
    response_model=UserGet,
    responses=responses,
    summary="Sign in a user",
)
async def login(request: Request,
                email: str,
                password: str,
                session: db_dependency):
    """Sign in a user"""
    user = await UserCRUD(session).select_one_or_none_filter_by(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User does not exist"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid password"
        )
    return user


@router.post(
    "/signup",
    responses=responses,
    response_model=UserGet,
    summary="Create User",
)
async def signup_user(
        session: db_dependency,
        password: str,
        phone_number: str,
        email: str,
):
    """Create User"""
    data = {
        "phone_number": phone_number,
        "email": email,
        "hashed_password": get_password_hash(password)
    }
    await validation_handler(pydantic_model=UserCreate, data=data)

    exist_user = await UserCRUD(session).select_all_filter_by(email=email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="A user with this email already exists"
        )

    user = await UserCRUD(session).create(**data)
    return user
