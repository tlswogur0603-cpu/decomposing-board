# 게시글 생성 비즈니스 로직을 담당.
# 현재 로그인 기능이 없어 author_id는 임시로 1로 지정.
# 실제 DB 저장은 post_repository에 위임.

from fastapi import HTTPException
from sqlalchemy.orm import Session
import math

from app.schemas.post import PostCreate, PostUpdate, PostPaginationResponse
from app.models.post import Post
from app.repositories.post_repository import create_post, fetch_posts_list, get_posts_count, get_post_by_id, update_post, delete_post

def create_post_service(
        db: Session,
        post: PostCreate,
) -> Post:
    author_id = 1 # TODO: 로그인 기능 구현 후 current_user.id로 교체

    return create_post(
        db=db,
        post=post,
        author_id=author_id,
    )

def get_posts_service(
        db: Session,
        limit: int,
        page: int,
) -> PostPaginationResponse:
    offset = (page - 1) * limit 

    items = fetch_posts_list(db=db, limit=limit, offset=offset)
    total_count = get_posts_count(db=db)
    total_pages = math.ceil(total_count / limit ) if total_count > 0 else 0

    return PostPaginationResponse(
        total_count=total_count,
        total_pages=total_pages,
        current_page=page,
        limit=limit,
        items=items,
    )

def get_post_detail_service(
        db: Session,
        post_id: int,
) -> Post:
    post = get_post_by_id(db=db, post_id=post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="게시글을 찾을 수 없습니다.",
        )
    
    return post

def update_post_service(
        db: Session,
        post_id: int,
        post_update: PostUpdate,
) -> Post:
    updated_post = update_post(db=db, post_id=post_id, post_update=post_update)

    if updated_post is None:
        raise HTTPException(
            status_code=404,
            detail="게시글을 찾을 수 없습니다.",
        ) 
    
    return updated_post

def delete_post_service(
        db: Session,
        post_id: int,
) -> Post:
    deleted_post = delete_post(db=db, post_id=post_id)

    if deleted_post is None:
        raise HTTPException(
            status_code=404,
            detail="게시글을 찾을 수 없습니다."
        )
    
    return deleted_post