# 게시글 API 라우터
# 요청 검증(PostCreate), DB 세션 주입(get_db), 서비스 로직 호출을 담당

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.post import PostCreate, PostRead
from app.core.database import get_db
from app.services.post_service import create_post_service

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
) -> PostRead:
    return create_post_service(db=db, post=post)