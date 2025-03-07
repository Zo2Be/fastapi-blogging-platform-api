import json
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_user
from api.dependencies.posts import post_by_id, check_post_author
from core.cache import get_redis_client
from core.config import settings
from core.constants import COMMON_RESPONSES
from core.logger import logger
from core.models import db_helper, User
from core.schemas.post import PostRead, PostCreate, PostUpdate
from crud import posts as posts_crud

router = APIRouter(prefix=settings.api.v1.posts, tags=["Posts"])


@router.get(
    "",
    response_model=list[PostRead],
    summary="Get all posts",
    description="Get list of posts with filtering and pagination",
)
async def get_posts(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    redis_client=Depends(get_redis_client),
    search: str = Query(
        None,
        min_length=2,
        description="Фильтрация постов по заголовку или категории (минимум 2 символа).",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Лимит постов на странице (1-100)",
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Смещение (начинается с 0)",
    ),
    order: str = Query(
        "id",
        enum=["id", "title", "created_at"],
        description="Сортировка по полю (id, title, created_at)",
    ),
):
    logger.info(
        "Get posts with params: search=%s, limit=%d, offset=%d, order=%s",
        search,
        limit,
        offset,
        order,
    )
    cache_key = f"posts_cache:{search}:{limit}:{offset}:{order}"
    cached = await redis_client.get(cache_key)
    if cached:
        posts = json.loads(cached)
        logger.info("Found %r cached posts", len(posts))
        return posts

    posts = await posts_crud.get_all_posts(
        session=session,
        search=search,
        limit=limit,
        offset=offset,
        order=order,
    )
    logger.info("Found %r posts", len(posts))
    posts_data = [
        PostRead.model_validate(post).model_dump(mode="json") for post in posts
    ]
    await redis_client.set(
        cache_key,
        json.dumps(posts_data),
        ex=settings.redis.ex,
    )
    logger.info("Saved %r for %r seconds", cache_key, settings.redis.ex)
    return posts


@router.get(
    "/{post_id}",
    response_model=PostRead,
    summary="Get post by ID",
    responses={
        status.HTTP_404_NOT_FOUND: COMMON_RESPONSES[status.HTTP_404_NOT_FOUND],
    },
)
async def get_post(
    post: Annotated[PostRead, Depends(post_by_id)],
):
    logger.info("Get post ID: %d", post.id)
    return post


@router.post(
    "",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create new post",
    responses={
        status.HTTP_401_UNAUTHORIZED: COMMON_RESPONSES[status.HTTP_401_UNAUTHORIZED]
    },
)
async def create_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    post_create: PostCreate,
):
    logger.info(
        "User %r creating new post with title: %r",
        user.id,
        post_create.title,
    )
    new_post = await posts_crud.create_post(
        session=session,
        post_create=post_create,
        user_id=user.id,
    )
    logger.info(
        "Post created successfully. ID: %r, Author: %r",
        new_post.id,
        user.id,
    )
    return new_post


@router.patch(
    "/{post_id}",
    response_model=PostRead,
    summary="Update existing post",
    responses=COMMON_RESPONSES,
)
async def update_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    post: Annotated[PostRead, Depends(post_by_id)],
    post_update: PostUpdate,
):
    logger.info(
        "User %r updating post ID: %r",
        user.id,
        post.id,
    )
    await check_post_author(
        user_id=user.id,
        post=post,
    )
    updated_post = await posts_crud.update_post(
        session=session,
        post=post,
        post_update=post_update,
    )
    logger.info(
        "Post ID %r updated successfully. Updated fields: %r by user with %r id",
        post.id,
        post_update.model_dump(exclude_unset=True),
        user.id,
    )
    return updated_post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete post",
    responses=COMMON_RESPONSES,
)
async def delete_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    post: Annotated[PostRead, Depends(post_by_id)],
) -> None:
    logger.info("Deleting post ID: %r", post.id)
    await check_post_author(
        user_id=user.id,
        post=post,
    )
    await posts_crud.delete_post(
        session=session,
        post=post,
    )
    logger.info(
        "Post ID %r deleted successfully by user with %r id",
        post.id,
        user.id,
    )
