# 게시글 API 라우터
# 요청 검증(PostCreate), DB 세션 주입(get_db), 서비스 로직 호출을 담당

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.schemas.post import PostCreate, PostRead, PostUpdate, PostPaginationResponse
from app.core.database import get_db
from app.services.post_service import create_post_service, get_posts_service, get_post_detail_service, update_post_service, delete_post_service

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
) -> PostRead:
    return create_post_service(db=db, post=post)

@router.get("", response_model=PostPaginationResponse, status_code=status.HTTP_200_OK)
def get_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db),
) -> PostPaginationResponse:
    return get_posts_service(db=db, page=page, limit=limit)

@router.get("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> PostRead:
    return get_post_detail_service(db=db, post_id=post_id)

@router.put("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
) -> PostRead:
    return update_post_service(db=db, post_id=post_id, post_update=post_update)

@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> None:
    delete_post_service(db=db, post_id=post_id)