import math

from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.repositories.post_repository import (
    create_post,
    delete_post,
    fetch_posts_list,
    get_post_by_id,
    get_posts_count,
    search_posts_repository,
    update_post,
)
from app.schemas.post import PostCreate, PostPaginationResponse, PostUpdate
from app.services.indexing_service import run_indexing


async def create_post_service(
    db: AsyncSession,
    post: PostCreate,
    background_tasks: BackgroundTasks,
) -> Post:
    author_id = 1

    new_post = await create_post(
        db=db,
        post=post,
        author_id=author_id,
    )

    await db.commit()
    await db.refresh(new_post)
    background_tasks.add_task(run_indexing, new_post.id)

    return new_post


async def get_posts_service(
    db: AsyncSession,
    limit: int,
    page: int,
) -> PostPaginationResponse:
    offset = (page - 1) * limit

    items = await fetch_posts_list(db=db, limit=limit, offset=offset)
    total_count = await get_posts_count(db=db)
    total_pages = math.ceil(total_count / limit) if total_count > 0 else 0

    return PostPaginationResponse(
        total_count=total_count,
        total_pages=total_pages,
        current_page=page,
        limit=limit,
        items=items,
    )


async def search_posts_service(db: AsyncSession, q: str) -> list[Post]:
    return await search_posts_repository(db=db, q=q)


async def get_post_detail_service(
    db: AsyncSession,
    post_id: int,
) -> Post:
    post = await get_post_by_id(db=db, post_id=post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="게시글을 찾을 수 없습니다.",
        )

    return post


async def update_post_service(
    db: AsyncSession,
    post_id: int,
    post_update: PostUpdate,
) -> Post:
    updated_post = await update_post(db=db, post_id=post_id, post_update=post_update)

    if updated_post is None:
        raise HTTPException(
            status_code=404,
            detail="게시글을 찾을 수 없습니다.",
        )

    await db.commit()
    await db.refresh(updated_post)
    return updated_post


async def delete_post_service(
    db: AsyncSession,
    post_id: int,
) -> Post:
    deleted_post = await delete_post(db=db, post_id=post_id)

    if deleted_post is None:
        raise HTTPException(
            status_code=404,
            detail="게시글을 찾을 수 없습니다.",
        )

    await db.commit()
    return deleted_post
