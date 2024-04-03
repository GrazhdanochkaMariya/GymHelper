from typing import Union

from fastapi import APIRouter, Path, HTTPException, status
from io import BytesIO
import pandas as pd

from src.api.api_dependencies import db_dependency
from src.api.utils import responses, send_single_email
from src.crud.user import UserCRUD
from src.crud.user_measurements import UserMeasurementsCRUD
from src.schemas.user_measurements import UserMeasurementsGet

router = APIRouter(tags=["User Measurements"])


@router.post(
    "/user-measurements",
    responses=responses,
    response_model=UserMeasurementsGet,
    summary="Create User measurements",
)
async def create_measurements(
    session: db_dependency,
    weight: Union[float, None],
    height: Union[float, None],
    biceps: Union[float, None],
    waist: Union[float, None],
    hips: Union[float, None],
    user_id: int,
):
    """Create measurements for User"""
    measurements_data = {
        "weight": weight,
        "height": height,
        "biceps": biceps,
        "waist": waist,
        "hips": hips,
        "user_id": user_id,
    }
    user_measurements = await UserMeasurementsCRUD(session).create(**measurements_data)
    return user_measurements


@router.get(
    "/user-measurements/{user_id}",
    responses=responses,
    response_model=list[UserMeasurementsGet],
    summary="Get all User measurements",
)
async def get_user_measurements(
    session: db_dependency, user_id: int = Path(ge=1, le=9223372036854775807)
):
    """Get all User measurements"""
    exist_user = await UserCRUD(session).select_all_filter_by(id=user_id)
    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_measurements = await UserMeasurementsCRUD(session).select_all_filter_by(
        user_id=user_id
    )
    return user_measurements


@router.get(
    "/user-measurements/export/{user_id}",
    responses=responses,
    summary="Send User measurements in excel to email",
)
async def export_to_excel_and_send_email(session: db_dependency, user_id: int):
    """Export user_measurements to an Excel file and send it to users email"""
    # TODO make as a background task
    user_measurements = await UserMeasurementsCRUD(session).select_all_filter_by(
        user_id=user_id
    )
    user = await UserCRUD(session).select_one_or_none_filter_by(id=user_id)

    data = [
        {
            "weight": user_measurement.weight,
            "height": user_measurement.height,
            "biceps": user_measurement.biceps,
            "waist": user_measurement.waist,
            "hips": user_measurement.hips,
            "created_at": user_measurement.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for user_measurement in user_measurements
    ]
    df = pd.DataFrame.from_records(data)
    # TODO integration with Amazon S3
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="Sheet1")
    excel_file.seek(0)
    send_single_email(email=user.email, attachment=excel_file)
    return None
