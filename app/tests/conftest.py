from typing import AsyncGenerator

import pytest
from fastapi_users.password import PasswordHelper
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from api.api_v1.fastapi_users import current_active_user
from core.models import Base, db_helper, User
from main import main_app

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5433/test_db"

engine_test: AsyncEngine = create_async_engine(TEST_DATABASE_URL, future=True)
SessionTesting = async_sessionmaker(
    bind=engine_test,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionTesting() as session:
        yield session
        await session.rollback()


@pytest.fixture()
async def test_user(session: AsyncSession):
    result = await session.execute(select(User).filter_by(email="test@example.com"))
    user = result.scalars().first()

    if user is None:
        password_helper = PasswordHelper()
        hashed_password = password_helper.hash("testpassword")

        user = User(
            email="test@example.com",
            hashed_password=hashed_password,
            is_active=True,
            is_verified=True,
            is_superuser=False,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


@pytest.fixture()
async def client(
    session: AsyncSession, test_user: User
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield session

    async def override_current_user():
        return test_user

    main_app.dependency_overrides[db_helper.session_getter] = override_get_session
    main_app.dependency_overrides[current_active_user] = override_current_user
    yield AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test",
    )
    del main_app.dependency_overrides[db_helper.session_getter]
    del main_app.dependency_overrides[current_active_user]
