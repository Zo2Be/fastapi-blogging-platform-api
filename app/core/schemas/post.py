from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class PostBase(BaseModel):
    title: str
    content: str | None = None
    category: str
    tags: list[str] | None = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    tags: list[str] | None = None


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    category: str
    tags: list[str] | None
    user: str
    created_at: datetime
    updated_at: datetime

    @field_validator("category", mode="before")
    def get_category(cls, value):
        return value.name if hasattr(value, "name") else "Unknown"

    @field_validator("user", mode="before")
    def get_user(cls, value):
        return value.email if hasattr(value, "email") else "Unknown"
