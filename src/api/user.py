from fastapi import APIRouter, Path, Query, HTTPException, status, Response

from src.api.utils import db_dependency, responses, validation_handler
from src.crud.user import UserCRUD
from src.schemas.user import UserGet, UserCreate

router = APIRouter(tags=["User"])


@router.get(
    "/users/{user_id}",
    responses=responses,
    response_model=UserGet,
    summary="Get User information",
)
async def get_user(session: db_dependency, user_id: int = Path(ge=1, le=9223372036854775807)):
    """Get User info"""
    user = await UserCRUD(session).select_one_or_none_filter_by(id=user_id)
    return user


@router.post(
    "/users",
    responses=responses,
    response_model=UserGet,
    summary="Create User",
)
async def create_user(
        session: db_dependency,
        phone_number: str = Query(),
        email: str = Query(),
):
    """Create User"""
    data = {
        "phone_number": phone_number,
        "email": email,
    }
    await validation_handler(pydantic_model=UserCreate, data=data)

    exist_user = await UserCRUD(session).select_all_filter_by(email=email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="A user with this email already exists"
        )

    user = await UserCRUD(session).create(**data)
    return user


@router.delete("/{playlist_id}", responses=responses)
async def delete_user_by_id(
    user_id: int,
    session: db_dependency,
):
    """Delete user"""

    exist_user = await UserCRUD(session).select_all_filter_by(id=user_id)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await UserCRUD(session).delete_rows_filer_by(id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
