from typing import Annotated

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Post
from core.types.user_id import UserIdType
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
    user_id: UserIdType,
    post: Post,
) -> None:
    if user_id != post.user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot change this post.",
        )
