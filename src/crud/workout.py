from datetime import datetime

from sqlalchemy import select, update
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

    async def select_all_filter_with_date(self, user_id, workout_date):
        query = (
            select(self.model)
            .options(selectinload(self.model.exercises))
            .where(self.model.user_id == user_id)
        )
        if workout_date:
            workout_date = datetime.strptime(workout_date, "%Y-%m-%d").date()
            query = query.where(Workout.workout_date == workout_date)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_status(self, workout_id):
        query = (
            update(self.model).where(self.model.id == workout_id).values(is_done=True)
        )

        await self.session.execute(query)
        await self.session.commit()
