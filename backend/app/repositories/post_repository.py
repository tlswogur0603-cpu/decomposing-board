# 게시글 DB 저장을 담당하는 파일
# PostCreate 요청 데이터를 Post ORM 객체로 변환한다.
# db 세션을 사용해 posts 테이블에 저장한다.
# 저장 후 DB에서 생성된 id, created_at 값을 반영한 Post 객체를 반환한다.

from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostPaginationResponse

# 게시글 생성: 요청 데이터를 Post ORM 객체로 변환해 DB에 저장
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

# 게시글 목록 조회(페이지네이션 적용): created_at 기준 내림차순 정렬 후 limit/offset 적용
def fetch_posts_list(db: Session, limit: int, offset: int) -> list[Post]:
    return (
        db.query(Post)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

# 게시글 전체 개수 조회
def get_posts_count(db: Session) -> int:
    return db.query(Post).count()

# 게시글 단일 조회: post_id와 일치하는 게시글 하나를 조회
def get_post_by_id(db: Session, post_id: int) -> Post | None:
    return db.query(Post).filter(Post.id == post_id).first()

# 게시글 수정: post_id로 게시글을 찾고 title/content를 수정
def update_post(
        db: Session,
        post_id: int,
        post_update: PostUpdate,
) -> Post | None:
    post = db.query(Post).filter(Post.id == post_id).first()

    if post is None:
        return None
    
    post.title = post_update.title
    post.content = post_update.content

    db.commit()
    db.refresh(post)

    return post

# 게시글 삭제: post_id로 게시글을 찾고 삭제
def delete_post(
        db: Session,
        post_id: int,
) -> Post | None:
    post = db.query(Post).filter(Post.id == post_id).first()

    if post is None:
        return None
    
    db.delete(post)
    db.commit()

    return post