from fastapi import APIRouter, Path, HTTPException, status, Response

from src.api.api_dependencies import db_dependency
from src.api.utils import responses
from src.crud.user import UserCRUD
from src.schemas.user import UserGet

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
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "/users",
    responses=responses,
    response_model=list[UserGet],
    summary="Get All Users",
)
async def get_all_users(session: db_dependency):
    """Get all Users from db"""
    users = await UserCRUD(session).select_all()
    return users


@router.delete("/{user_id}", responses=responses)
async def delete_user_by_id(
    user_id: int,
    session: db_dependency,
):
    """Delete user"""

    exist_user = await UserCRUD(session).select_one_or_none_filter_by(id=user_id)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await UserCRUD(session).delete_rows_filer_by(id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
