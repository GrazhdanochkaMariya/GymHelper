from fastapi import APIRouter, Path, HTTPException, status

from src.api.utils import db_dependency, responses
from src.crud.user import UserCRUD
from src.crud.user_measurements import UserMeasurementsCRUD
from src.schemas.user_measurements import UserMeasurementsGet

router = APIRouter(tags=["User Measurements"])


@router.get(
    "/user-measurements/{user_id}",
    responses=responses,
    response_model=list[UserMeasurementsGet],
    summary="Get all User measurements",
)
async def get_user_measurements(session: db_dependency, user_id: int = Path(ge=1, le=9223372036854775807)):
    """Get all User measurements"""
    exist_user = await UserCRUD(session).select_all_filter_by(id=user_id)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_measurements = await UserMeasurementsCRUD(session).select_all_filter_by(user_id=user_id)
    return user_measurements


