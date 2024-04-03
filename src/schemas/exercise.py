from typing import Union

from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    name: str
    description: Union[str, None] = None
    sets: int
    repetitions: int


class ExerciseGet(ExerciseCreate):
    id: int
