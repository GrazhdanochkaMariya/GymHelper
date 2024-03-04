from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import BaseCRUD
from src.models.workout import Exercise


class ExerciseCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Exercise, session=session)
