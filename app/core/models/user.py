from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
)

from .base import Base
from .mixins.int_id_pk import IntIdPKMixin


class User(Base, IntIdPKMixin, SQLAlchemyBaseUserTable[int]):
    pass
