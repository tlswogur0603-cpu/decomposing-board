from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.ai import PostIndexResponse
from app.repositories.post_repository import get_post_by_id
from app.repositories.vector_repository import save_post_to_vector_store

def index_single_post_service(db: Session, post_id: int) -> PostIndexResponse:
    post = get_post_by_id(db=db, post_id=post_id)
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 게시글을 찾을 수 없습니다.",
        )

    save_post_to_vector_store(
        post_id=post.id,
        title=post.title,
        content=post.content,
    )

    return PostIndexResponse(
        indexed_count=1,
        message="게시글 인덱싱이 완료되었습니다.",
    )