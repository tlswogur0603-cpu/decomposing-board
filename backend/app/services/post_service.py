# 게시글 생성 비즈니스 로직을 담당.
# 현재 로그인 기능이 없어 author_id는 임시로 1로 지정.
# 실제 DB 저장은 post_repository에 위임.

from sqlalchemy.orm import Session
from app.schemas.post import PostCreate
from app.models.post import Post
from app.repositories.post_repository import create_post

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