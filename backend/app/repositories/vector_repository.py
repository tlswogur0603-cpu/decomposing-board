import asyncio

from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.core.constants import POST_CHUNK_OVERLAP, POST_CHUNK_SIZE
from backend.app.rag.embedding import get_embedding_model
from backend.app.rag.chunking import split_post_content

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
) -> int:
    vector_store = get_vector_store()
    await delete_post_from_vector_store(post_id=post_id, vector_store=vector_store)

    chunks = split_post_content(content=content)
    chunk_count = len(chunks)
    document_title = title or "제목 없음"

    documents = [
        Document(
            page_content=(
                f"제목: {document_title}\n"
                f"청크: {chunk_index + 1}/{chunk_count}\n"
                f"내용: {chunk}"
            ),
            metadata={
                "post_id": post_id,
                "chunk_index": chunk_index,
                "chunk_count": chunk_count,
                "title": document_title,
                "content": chunk,
                "chunk_size": POST_CHUNK_SIZE,
                "chunk_overlap": POST_CHUNK_OVERLAP,
            },
        )
        for chunk_index, chunk in enumerate(chunks)
    ]
    ids = [
        f"post-{post_id}-chunk-{chunk_index}"
        for chunk_index in range(chunk_count)
    ]

    await _add_documents(
        vector_store=vector_store,
        documents=documents,
        ids=ids,
    )

    return chunk_count


async def delete_post_from_vector_store(
    post_id: int,
    vector_store: Chroma | None = None,
) -> None:
    vector_store = vector_store or get_vector_store()
    chunk_ids = await _get_post_vector_ids(vector_store=vector_store, post_id=post_id)

    if not chunk_ids:
        return

    await _delete_documents(vector_store=vector_store, ids=chunk_ids)


async def _add_documents(
    vector_store: Chroma,
    documents: list[Document],
    ids: list[str],
) -> None:
    if hasattr(vector_store, "aadd_documents"):
        await vector_store.aadd_documents(
            documents=documents,
            ids=ids,
        )
        return

    await asyncio.to_thread(
        vector_store.add_documents,
        documents=documents,
        ids=ids,
    )


async def _get_post_vector_ids(vector_store: Chroma, post_id: int) -> list[str]:
    if hasattr(vector_store, "aget"):
        result = await vector_store.aget(where={"post_id": post_id})
    else:
        result = await asyncio.to_thread(vector_store.get, where={"post_id": post_id})

    return list(result.get("ids") or [])


async def _delete_documents(vector_store: Chroma, ids: list[str]) -> None:
    if hasattr(vector_store, "adelete"):
        await vector_store.adelete(ids=ids)
        return

    await asyncio.to_thread(vector_store.delete, ids=ids)


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
