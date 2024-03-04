from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import BaseCRUD
from src.models.user import UserMeasurements


class UserMeasurementsCRUD(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserMeasurements, session=session)
