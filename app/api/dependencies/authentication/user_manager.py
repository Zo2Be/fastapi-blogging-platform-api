from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from core.authentication.user_manager import UserManager

from .users import get_users_db

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(
    user_db: Annotated[
        "SQLAlchemyUserDatabase",
        Depends(get_users_db),
    ],
):
    yield UserManager(user_db)
