import asyncio

from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.services.embedding_service import get_embedding_model

COLLECTION_NAME = "traceboard_posts"
PERSIST_DIRECTORY = "./chroma_db"


def get_vector_store() -> Chroma:
    embedding_model = get_embedding_model()
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model,
    )


async def save_post_to_vector_store(
    post_id: int,
    title: str | None,
    content: str,
) -> None:
    vector_store = get_vector_store()
    document_text = f"제목: {title or '제목 없음'}\n내용: {content}"

    document = Document(
        page_content=document_text,
        metadata={
            "post_id": post_id,
            "title": title or "제목 없음",
            "content": content,
        },
    )

    await vector_store.aadd_documents(
        documents=[document],
        ids=[f"post-{post_id}"],
    )


async def search_similar_posts(
    question: str,
    top_k: int = 3,
) -> list[Document]:
    vector_store = get_vector_store()
    if hasattr(vector_store, "asimilarity_search"):
        return await vector_store.asimilarity_search(
            query=question,
            k=top_k,
        )

    return await asyncio.to_thread(
        vector_store.similarity_search,
        query=question,
        k=top_k,
    )
