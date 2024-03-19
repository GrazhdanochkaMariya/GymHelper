import pytest

from src.crud.user import UserCRUD


@pytest.mark.asyncio
async def test_select_all_emails(db_session):
    user_crud = UserCRUD(session=db_session)
    result = await user_crud.select_all_emails()
    assert len(result) == 2


@pytest.mark.asyncio
async def test_update_delete_field(db_session):
    user_crud = UserCRUD(session=db_session)
    user_id = 1

    await user_crud.update_delete_field(user_id=user_id)
    deleted_user = await user_crud.select_one_or_none_filter_by(id=user_id)

    assert deleted_user.id == 1
    assert deleted_user.deleted_at
