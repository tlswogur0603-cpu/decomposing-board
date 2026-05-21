# vector_repository는 Chroma에 게시글을 저장하고, 질문과 유사한 게시글을 검색한다.

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

def save_post_to_vector_store(
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

    vector_store.add_documents(
        documents=[document],
        ids=[f"post-{post_id}"],
    )

def search_similar_posts(
        question: str,
        top_k: int = 3,
) -> list[Document]:
    vector_store = get_vector_store()

    return vector_store.similarity_search(
        query=question,
        k=top_k,
    )