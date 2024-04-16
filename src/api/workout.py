import datetime
from pathlib import Path
from typing import Union

from fastapi import APIRouter, HTTPException, status, Request

from src.api.api_dependencies import db_dependency
from src.api.utils import responses, update_user_level
from src.crud.user import UserCRUD
from src.crud.workout import WorkoutCRUD
from src.pages.pages import templates
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


@router.get(
    "/workout/{user_id}",
    responses=responses,
    summary="Get all User workouts",
)
async def get_user_workouts(
    request: Request,
    session: db_dependency,
    workout_date: str,
    user_id: int = Path(ge=1, le=9223372036854775807),
):
    """Get all User measurements"""
    # TODO add pagination
    exist_user = await UserCRUD(session).select_all_filter_by(id=user_id)
    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    workouts = await WorkoutCRUD(session).select_all_filter_with_date(
        user_id=user_id, workout_date=workout_date
    )
    return templates.TemplateResponse(
        "user_workouts.html",
        {"request": request, "workouts": workouts, "user": exist_user},
    )


@router.post(
    "/workout/done",
    responses=responses,
    summary="Change status is_done",
)
async def change_status(session: db_dependency, workout_id: int, user_id: int):
    """Change workout status is_done"""

    user = await UserCRUD(session).select_one_or_none_filter_by(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    workout = await WorkoutCRUD(session).select_one_or_none_filter_by(id=workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found"
        )
    new_score = user.score + 1 if user.score else 1
    new_level = update_user_level(new_score)
    await WorkoutCRUD(session).update_status(workout_id=workout_id)
    await UserCRUD(session).update(
        item_id=user_id, score=new_score, score_level=new_level
    )

    return None
