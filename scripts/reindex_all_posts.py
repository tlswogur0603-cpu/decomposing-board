"""PostgreSQL의 모든 게시글을 현재 임베딩 설정으로 재인덱싱한다.

예시:
    python scripts/reindex_all_posts.py --provider huggingface
    python scripts/reindex_all_posts.py --provider huggingface --model-name BAAI/bge-m3
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
for import_path in (PROJECT_ROOT, BACKEND_ROOT):
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="전체 게시글 벡터 재인덱싱")
    parser.add_argument(
        "--provider",
        choices=("gemini", "huggingface"),
        help="재인덱싱에 사용할 임베딩 provider (기본값: 환경 설정)",
    )
    parser.add_argument(
        "--model-name",
        help="Hugging Face 모델명 (provider가 huggingface일 때 선택)",
    )
    parser.add_argument(
        "--collection-name",
        help="저장할 Chroma 컬렉션명 (선택)",
    )
    return parser.parse_args()


async def reindex_all_posts() -> int:
    from backend.app.core.database import AsyncSessionLocal
    from backend.app.repositories.post_repository import fetch_all_posts
    from backend.app.services.rag_service import index_single_post_service

    failures: list[int] = []
    indexed_posts = 0
    async with AsyncSessionLocal() as db:
        posts = await fetch_all_posts(db)
        print(f"재인덱싱 대상 게시글: {len(posts)}개")

        for post in posts:
            try:
                result = await index_single_post_service(db=db, post_id=post.id)
                indexed_posts += 1
                print(
                    f"✅ post_id={post.id}, chunk_count={result.indexed_count}"
                )
            except Exception:
                failures.append(post.id)
                print(f"❌ post_id={post.id} 인덱싱 실패", file=sys.stderr)

    print(f"완료: {indexed_posts}/{len(posts)}개 게시글")
    if failures:
        print(f"실패한 post_id: {', '.join(map(str, failures))}", file=sys.stderr)
        return 1
    return 0


def main() -> None:
    args = parse_args()
    if args.provider:
        os.environ["EMBEDDING_PROVIDER"] = args.provider
    if args.model_name:
        os.environ["HF_MODEL_NAME"] = args.model_name
    if args.collection_name:
        os.environ["CHROMA_COLLECTION_NAME"] = args.collection_name

    raise SystemExit(asyncio.run(reindex_all_posts()))


if __name__ == "__main__":
    main()
