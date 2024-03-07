from datetime import date, datetime, time
from typing import List, Union

from pydantic import BaseModel, field_validator

from src.schemas.exercise import ExerciseGet


class WorkoutCreate(BaseModel):
    date: date
    time: time

    @field_validator("date")
    def parse_date(cls, v: str):
        if isinstance(v, str):
            try:
                workout_date = datetime.strptime(v, "%d.%m.%Y")
                return workout_date.date()
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY format.")
        return v

    @field_validator("time")
    def parse_time(cls, v):
        if isinstance(v, str):
            try:
                workout_time = datetime.strptime(v, "%H:%M")
                return workout_time.time()
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM format.")
        return v


class WorkoutGet(WorkoutCreate):
    id: int
    exercises: Union[List[ExerciseGet], None] = None
