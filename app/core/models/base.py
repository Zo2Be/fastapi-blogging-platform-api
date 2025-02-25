from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from core.config import settings
from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_conventions,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        table_name = camel_case_to_snake_case(cls.__name__)
        if table_name.endswith("y"):
            return f"{table_name[:-1]}ies"
        return f"{table_name}s"
