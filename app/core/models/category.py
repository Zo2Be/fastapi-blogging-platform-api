from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPKMixin

if TYPE_CHECKING:
    from .post import Post


class Category(IntIdPKMixin, Base):
    name: Mapped[str] = mapped_column(String(15), unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="category")
