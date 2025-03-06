from sqlalchemy import select, or_, Select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Post, Category
from core.schemas.post import PostCreate, PostUpdate
from core.types.user_id import UserIdType


async def get_all_posts(
    session: AsyncSession,
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
    order: str = "id",
) -> list[Post]:
    statement = (
        select(Post)
        .options(
            selectinload(Post.category),
            selectinload(Post.user),
        )
        .order_by(Post.id)
    )

    if search:
        statement = statement.where(
            or_(
                Post.title.ilike(f"%{search}%"),
                Post.category.has(Category.name.ilike(f"%{search}%")),
            )
        )
    statement = apply_ordering(statement, order)
    statement = statement.limit(limit).offset(offset)

    result: Result = await session.execute(statement)
    posts = result.scalars().all()
    return list(posts)


def apply_ordering(statement: Select, order: str) -> Select:
    if order == "title":
        return statement.order_by(Post.title.asc())
    if order == "created_at":
        return statement.order_by(Post.created_at.desc())
    return statement.order_by(Post.id.asc())


async def get_post_by_id(
    session: AsyncSession,
    post_id: int,
) -> Post | None:
    statement = (
        select(Post)
        .options(selectinload(Post.category), selectinload(Post.user))
        .where(Post.id == post_id)
    )
    result = await session.execute(statement)
    post = result.scalar_one_or_none()
    return post


async def create_post(
    session: AsyncSession,
    post_create: PostCreate,
    user_id: UserIdType,
):
    category = await get_or_create_category(
        session=session,
        category_name=post_create.category,
    )
    post_data = post_create.model_dump()
    post_data.pop("category", None)
    post = Post(
        **post_data,
        user_id=user_id,
        category_id=category.id,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    stmt = (
        select(Post)
        .options(selectinload(Post.category), selectinload(Post.user))
        .where(Post.id == post.id)
    )
    result = await session.execute(stmt)
    post = result.scalar_one()
    return post


async def update_post(
    session: AsyncSession,
    post: Post,
    post_update: PostUpdate,
) -> Post:
    update_data = post_update.model_dump(exclude_unset=True)
    if "category" in update_data:
        category_name = update_data.pop("category")
        category = await get_or_create_category(
            session=session,
            category_name=category_name,
        )
        post.category_id = category.id

    for name, value in update_data.items():
        setattr(post, name, value)
    await session.commit()
    await session.refresh(post)
    return post


async def delete_post(
    session: AsyncSession,
    post: Post,
) -> None:
    await session.delete(post)
    await session.commit()


async def get_or_create_category(
    session: AsyncSession,
    category_name: str,
) -> Category:
    statement = select(Category).where(Category.name == category_name)
    result: Result = await session.execute(statement)
    category = result.scalar_one_or_none()
    if not category:
        category = Category(name=category_name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
    return category
