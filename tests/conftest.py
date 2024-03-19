import datetime
from random import randint
from string import ascii_letters
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import settings
from main import app
from src.db.session import Base, get_db_session
from src.models import User


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    DATABASE_URL = settings.get_async_test_database_url()
    engine = create_async_engine(DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()

    user_data1 = get_user_data()
    user1 = User(**user_data1)
    session.add(user1)
    await session.commit()

    user_data2 = get_user_data()
    user2 = User(**user_data2)
    session.add(user2)
    await session.commit()

    yield session
    await session.close()


@pytest.fixture()
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_db_session] = lambda: db_session
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


def get_user_data() -> dict:
    return {
        "email": f"user{randint(100, 999)}@example.com",
        "phone_number": f"+1234567890{randint(0, 9)}",
        "hashed_password": "".join(
            [ascii_letters[randint(0, len(ascii_letters) - 1)] for _ in range(10)]
        ),
        "created_at": datetime.datetime.now(),
    }
