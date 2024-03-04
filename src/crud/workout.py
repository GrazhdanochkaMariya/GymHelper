from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import BaseCRUD
from src.models.workout import Workout


class WorkoutCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Workout, session=session)
