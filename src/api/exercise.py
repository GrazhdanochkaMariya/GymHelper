from typing import Union

from fastapi import APIRouter

from src.api.api_dependencies import db_dependency
from src.api.utils import responses
from src.crud.exercise import ExerciseCRUD
from src.schemas.exercise import ExerciseGet

router = APIRouter(tags=["Exercise"])


@router.post(
    "/exercises",
    responses=responses,
    response_model=ExerciseGet,
    summary="Create exercise",
)
async def create_exercise(
    session: db_dependency,
    name: str,
    description: Union[str, None],
    sets: int,
    repetitions: int,
    workout_id: int,
):
    """Create exercise for User workout"""
    exercise_data = {
        "name": name,
        "description": description,
        "sets": sets,
        "repetitions": repetitions,
        "workout_id": workout_id,
    }
    exercise = await ExerciseCRUD(session).create(**exercise_data)
    return exercise


@router.get(
    "/exercises/{workout_id}",
    responses=responses,
    summary="Get all exercises by workout id",
)
async def get_workout_exercises(
    session: db_dependency,
    workout_id: int,
):
    """Get all exercises for User workout by workout id"""

    exercises = await ExerciseCRUD(session).select_all_filter_by(workout_id=workout_id)
    return exercises
