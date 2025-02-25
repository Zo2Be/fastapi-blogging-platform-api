from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, String, Text, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.user_id import UserIdType
from .base import Base
from .mixins.int_id_pk import IntIdPKMixin

if TYPE_CHECKING:
    from .user import User
    from .category import Category


class Post(IntIdPKMixin, Base):
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
        nullable=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        index=True,
    )
    tags: Mapped[list[str]] = mapped_column(
        ARRAY(String(50)),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    user_id: Mapped[UserIdType] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="posts")
    category: Mapped["Category"] = relationship(back_populates="posts")
