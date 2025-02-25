from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_user
from core.config import settings
from core.models import db_helper, User
from core.schemas.post import PostRead, PostCreate, PostUpdate

from crud import posts as posts_crud
from api.dependencies.posts import post_by_id, check_post_author

router = APIRouter(prefix=settings.api.v1.posts, tags=["Posts"])


@router.get("", response_model=list[PostRead])
async def get_posts(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    search: str = Query(
        None,
        description="Фильтрация постов по заголовку или категории.",
    ),
):
    if search:
        posts = await posts_crud.search_posts(session=session, search=search)
    else:
        posts = await posts_crud.get_all_posts(session=session)
    return posts


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post: Annotated[PostRead, Depends(post_by_id)],
):
    return post


@router.post("", response_model=PostRead)
async def create_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    post_create: PostCreate,
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
):
    return await posts_crud.create_post(
        session=session,
        post_create=post_create,
        user_id=user.id,
    )


@router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    post: Annotated[PostRead, Depends(post_by_id)],
    post_update: PostUpdate,
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
):
    await check_post_author(
        user_id=user.id,
        post=post,
    )
    return await posts_crud.update_post(
        session=session,
        post=post,
        post_update=post_update,
    )


@router.delete("/{post_id}")
async def delete_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    post: Annotated[PostRead, Depends(post_by_id)],
) -> None:
    return await posts_crud.delete_post(
        session=session,
        post=post,
    )
