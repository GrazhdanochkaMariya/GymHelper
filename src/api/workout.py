import datetime
from typing import Union

from fastapi import APIRouter

from src.api.api_dependencies import db_dependency
from src.api.utils import responses
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
    workout_date: Union[str, None],
    workout_time: Union[str, None],
    user_id: int,
):
    """Create workout for User"""
    w_date = datetime.datetime.strptime(workout_date, "%d.%m.%Y").date()
    w_time = datetime.datetime.strptime(workout_time, "%H.%M").time()
    workout_data = {
        "name": name,
        "description": description,
        "workout_date": w_date,
        "workout_time": w_time,
        "user_id": user_id,
    }
    workout = await WorkoutCRUD(session).create(**workout_data)
    return workout
