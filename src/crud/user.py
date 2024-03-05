from sqlalchemy import select
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
