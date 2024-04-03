from datetime import date, datetime, time

from pydantic import BaseModel, field_validator


class WorkoutCreate(BaseModel):
    description: str
    name: str
    workout_date: date
    workout_time: time
    user_id: int

    @field_validator("workout_date")
    def parse_date(cls, v: str):
        if isinstance(v, str):
            try:
                workout_date = datetime.strptime(v, "%d.%m.%Y")
                return workout_date.date()
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY format.")
        return v

    @field_validator("workout_time")
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
