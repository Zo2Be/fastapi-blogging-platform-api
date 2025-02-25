from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.orm import Mapped, relationship

from core.types.user_id import UserIdType
from .base import Base
from .mixins.int_id_pk import IntIdPKMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .post import Post


class User(Base, IntIdPKMixin, SQLAlchemyBaseUserTable[UserIdType]):
    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
