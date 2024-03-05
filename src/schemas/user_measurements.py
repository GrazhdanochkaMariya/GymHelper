from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserMeasurementsGet(BaseModel):
    """Schema for user measurements"""
    id: int
    user_id: int
    weight: float
    height: float
    biceps: float
    waist: float
    hips: float
    created_at: datetime
    deleted_at: Optional[datetime] = None

    model_config: dict = {"from_attributes": True}