from typing import Union

from fastapi import APIRouter

from src.api.api_dependencies import db_dependency
from src.api.utils import responses
from src.crud.exercise import ExerciseCRUD
from src.schemas.exercise import ExerciseGet

router = APIRouter(tags=["Exercise"])


@router.post(
    "/exercise",
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
