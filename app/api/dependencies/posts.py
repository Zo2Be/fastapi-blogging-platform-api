from typing import Annotated

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_user
from core.models import db_helper, Post, User
from crud import posts


async def post_by_id(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    post_id: int,
) -> Post:
    post = await posts.get_post_by_id(
        session=session,
        post_id=post_id,
    )
    if post is None:
        raise HTTPException(
            status_code=404,
            detail=f"Post {post_id} not found",
        )
    return post


async def check_post_author(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    post: Annotated[
        Post,
        Depends(post_by_id),
    ],
) -> tuple[User, Post]:
    if user.id != post.user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot change this post.",
        )
    return user, post
