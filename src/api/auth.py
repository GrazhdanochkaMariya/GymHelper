from fastapi import APIRouter, Request

from src.api.utils import responses, db_dependency
from src.schemas.user import UserCreate

router = APIRouter(tags=["Authentication"])


# @router.post(
#     "/login",
#     responses=responses,
#     summary="Sign Up or Sign in a user",
# )
# async def login(request: Request, user: UserCreate, db: db_dependency):
#     # """Creates user and sends access code"""
#     # logout_logger.info(
#     #         f"Before check beeline user"
#     #     )
#     is_beeline_user = await check_beeline_user(user.phone_number)
#     operator = OperatorEnum.BEELINE if is_beeline_user else OperatorEnum.ANOTHER
#
#     db_user = await crud_user.get_user_devices_by_phone_number(db, phone_number=user.phone_number)
#     verification_code = await get_code()
#
#     if not db_user:
#         new_user = await crud_user.create(
#             db,
#             new_data={
#                 "phone_number": user.phone_number,
#                 "operator": operator,
#                 "is_active": False,
#                 "verification_code": verification_code,
#             },
#         )
#         await device_crud_base.create(
#             db,
#             new_data={
#                 "user_id": new_user.id,
#                 "device_id": user.device_id,
#                 "device_name": user.device_name,
#             },
#         )
#
#         await send_smsc_message(request, new_user.id, verification_code, user.phone_number)
#         return {"message": USER_CREATED_MESSAGE, "first_time": True}
#
#     await user_crud_base.update(db, item=db_user, new_data={"verification_code": verification_code, "last_activity": datetime.now()})
#     await send_smsc_message(request, db_user.id, verification_code, user.phone_number)
#
#     if user.device_id not in [device.device_id for device in db_user.devices]:
#         await device_crud_base.create(
#             db,
#             new_data={
#                 "user_id": db_user.id,
#                 "device_id": user.device_id,
#                 "device_name": user.device_name,
#             },
#         )
#
#         return {"message": USER_CREATED_MESSAGE, "first_time": True}
#
#     return {"message": CODE_SENT_MESSAGE}