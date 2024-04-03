from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.crud.base import BaseCRUD
from src.models.workout import Workout


class WorkoutCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Workout, session=session)

    async def select_users_workouts_by_user_id(self, user_id):
        query = (
            select(self.model)
            .options(selectinload(self.model.exercises))
            .where(self.model.user_id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
