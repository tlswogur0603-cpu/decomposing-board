# 게시글 DB 저장을 담당하는 파일
# PostCreate 요청 데이터를 Post ORM 객체로 변환한다.
# db 세션을 사용해 posts 테이블에 저장한다.
# 저장 후 DB에서 생성된 id, created_at 값을 반영한 Post 객체를 반환한다.

from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate

def create_post(
        db: Session,
        post: PostCreate,
        author_id: int,
) -> Post:
    new_post = Post(
        title=post.title,
        content=post.content,
        author_id=author_id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

def get_posts(db: Session) -> list[Post]:
    return db.query(Post).order_by(Post.created_at.desc()).all()

def get_post_by_id(db: Session, post_id: int) -> Post | None:
    return db.query(Post).filter(post_id == post_id).first()