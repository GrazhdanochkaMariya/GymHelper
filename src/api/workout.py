from typing import Union

from fastapi import APIRouter, Path, HTTPException, status

from src.api.api_dependencies import db_dependency
from src.api.utils import responses
from src.crud.user import UserCRUD
from src.crud.workout import WorkoutCRUD
from src.schemas.workout import WorkoutGet

router = APIRouter(tags=["Workout"])


@router.post(
    "/workout",
    responses=responses,
    response_model=WorkoutGet,
    summary="Create workout",
)
async def create_workout(
    session: db_dependency,
    name: Union[str, None],
    description: Union[str, None],
    date: Union[str, None],
    time: Union[str, None],
    user_id: int,
):
    """Create workout for User"""
    workout_data = {
        "name": name,
        "description": description,
        "date": date,
        "time": time,
        "user_id": user_id,
    }
    workout = await WorkoutCRUD(session).create(**workout_data)
    return workout


@router.get(
    "/workout/{user_id}",
    responses=responses,
    response_model=list[WorkoutGet],
    summary="Get all User workouts",
)
async def get_user_workouts(
    session: db_dependency, user_id: int = Path(ge=1, le=9223372036854775807)
):
    """Get all User workouts"""
    exist_user = await UserCRUD(session).select_all_filter_by(id=user_id)
    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_workouts = await WorkoutCRUD(session).select_all_filter_by(user_id=user_id)
    return user_workouts
