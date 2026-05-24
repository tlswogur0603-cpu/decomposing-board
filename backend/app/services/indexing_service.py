from app.services.rag_service import index_single_post_service

async def run_indexing(db, post_id: int):
    await index_single_post_service(db, post_id)