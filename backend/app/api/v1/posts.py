from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.post import PostCreate, PostPaginationResponse, PostRead, PostUpdate
from app.services.post_service import (
    create_post_service,
    delete_post_service,
    get_post_detail_service,
    get_posts_service,
    search_posts_service,
    update_post_service,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> PostRead:
    return await create_post_service(db=db, post=post, background_tasks=background_tasks)


@router.get("", response_model=PostPaginationResponse, status_code=status.HTTP_200_OK)
async def get_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
) -> PostPaginationResponse:
    return await get_posts_service(db=db, page=page, limit=limit)


@router.get("/search", response_model=list[PostRead], status_code=status.HTTP_200_OK)
async def search_posts(
    q: str = Query(default="", max_length=50, description="검색할 문자열"),
    db: AsyncSession = Depends(get_db),
) -> list[PostRead]:
    return await search_posts_service(db=db, q=q)


@router.get("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
) -> PostRead:
    return await get_post_detail_service(db=db, post_id=post_id)


@router.put("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> PostRead:
    return await update_post_service(
        db=db,
        post_id=post_id,
        post_update=post_update,
        background_tasks=background_tasks,
    )


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> None:
    await delete_post_service(
        db=db,
        post_id=post_id,
        background_tasks=background_tasks,
    )
