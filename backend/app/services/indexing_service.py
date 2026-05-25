from app.services.rag_service import index_single_post_service
from app.core.database import AsyncSessionLocal

async def run_indexing(post_id: int):
    async with AsyncSessionLocal() as db:
        await index_single_post_service(db, post_id)