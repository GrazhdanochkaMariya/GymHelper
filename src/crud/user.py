import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import BaseCRUD
from src.models.user import User


class UserCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def select_all_emails(self):
        query = select(self.model.email)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_delete_field(self, user_id: int):
        query = (
            update(self.model)
            .where(self.model.id == user_id)
            .values({"deleted_at": datetime.datetime.now()})
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result

    async def update_score(self, user_id: int):
        user = await self.select_one_or_none_filter_by(id=user_id)
        if user:
            current_score = user.score or 0
            new_score = current_score + 1
            query = (
                update(self.model)
                .where(self.model.id == user_id)
                .values(score=new_score)
            )
            await self.session.execute(query)
            await self.session.commit()

    async def update_avatar(self, user_id: int, avatar_path: str):
        query = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(avatar_path=avatar_path)
        )
        await self.session.execute(query)
        await self.session.commit()
