from app.services.rag_service import index_single_post_service
from app.repositories.vector_repository import delete_post_from_vector_store
from app.core.database import AsyncSessionLocal


async def run_indexing(post_id: int):
    async with AsyncSessionLocal() as db:
        await index_single_post_service(db, post_id)


async def delete_post_index(post_id: int):
    await delete_post_from_vector_store(post_id=post_id)
