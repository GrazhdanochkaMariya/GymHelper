from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import BaseCRUD
from src.models.user import User


class UserCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)
