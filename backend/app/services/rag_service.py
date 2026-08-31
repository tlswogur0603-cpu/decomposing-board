from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.ai import AIQueryResponse, PostIndexResponse, SourcePost
from app.repositories.post_repository import get_post_by_id
from app.repositories.vector_repository import save_post_to_vector_store, search_similar_posts
from app.rag.llm import generate_answer
from app.core.logging import get_logger

logger = get_logger(__name__)

async def index_single_post_service(db: AsyncSession, post_id: int) -> PostIndexResponse:
    logger.info(f"🔥 indexing start: {post_id}")
    post = await get_post_by_id(db=db, post_id=post_id)
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 게시글을 찾을 수 없습니다.",
        )

    try:
        indexed_count = await save_post_to_vector_store(
            post_id=post.id,
            title=post.title,
            content=post.content,
        )
    except Exception:
        logger.exception("❌ indexing failed: post_id=%s", post.id)
        raise

    logger.info(
        "✅ indexing completed: post_id=%s, chunk_count=%s",
        post.id,
        indexed_count,
    )

    return PostIndexResponse(
        indexed_count=indexed_count,
        message="게시글 인덱싱이 완료되었습니다.",
    )


async def answer_question_service(question: str) -> AIQueryResponse:
    related_documents = await search_similar_posts(question=question, top_k=3)

    if not related_documents:
        return AIQueryResponse(
            answer="관련된 기록을 찾지 못했습니다.",
            sources=[],
        )

    context = "\n\n".join(
        f"[참고자료 {idx}]\n{document.page_content}"
        for idx, document in enumerate(related_documents, start=1)
    )

    answer = await generate_answer(context=context, question=question)

    sources = [
        SourcePost(
            post_id=document.metadata.get("post_id"),
            title=document.metadata.get("title"),
            chunk_index=document.metadata.get("chunk_index"),
            chunk_count=document.metadata.get("chunk_count"),
        )
        for document in related_documents
        if document.metadata is not None and document.metadata.get("post_id") is not None
    ]

    return AIQueryResponse(
        answer=answer,
        sources=sources,
    )
