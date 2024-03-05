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

    async def update_delete_field(
        self, user_id: str
    ):
        query = (
            update(self.model)
            .where(self.model.id == user_id)
            .values({"deleted_at": datetime.datetime.now()})
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result