from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ai import AIQueryRequest, AIQueryResponse, PostIndexResponse
from app.services.rag_service import answer_question_service, index_single_post_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/index-post/{post_id}",response_model=PostIndexResponse,status_code=status.HTTP_200_OK,)
def index_post(
    post_id: int, 
    db: Session = Depends(get_db),
) -> PostIndexResponse:
    return index_single_post_service(db=db, post_id=post_id)

@router.post("/query",response_model=AIQueryResponse,status_code=status.HTTP_200_OK,)
def query_ai(
    request: AIQueryRequest,
) -> AIQueryResponse:
    return answer_question_service(question=request.question)
