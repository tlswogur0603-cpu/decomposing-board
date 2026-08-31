from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_chroma import Chroma


COLLECTION_NAME = "traceboard_posts"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _persist_directory() -> str:
    return str(_project_root() / "chroma_db")


def _preview_text(text: str, limit: int = 80) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[:limit].rstrip() + "..."


def _safe_get(items: list[Any], index: int, default: Any = None) -> Any:
    if index >= len(items):
        return default
    return items[index]


def main() -> None:
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=_persist_directory(),
    )

    result = vector_store.get(include=["documents", "metadatas"])

    ids = result.get("ids") or []
    documents = result.get("documents") or []
    metadatas = result.get("metadatas") or []

    rows: list[dict[str, Any]] = []
    chunk_count_by_post_id: dict[Any, int] = {}
    for index, chunk_id in enumerate(ids):
        metadata = _safe_get(metadatas, index, {}) or {}
        document = _safe_get(documents, index, "") or ""
        raw_content = metadata.get("content") or document
        chunk_length = len(str(raw_content))
        post_id = metadata.get("post_id")

        if post_id is not None:
            chunk_count_by_post_id[post_id] = chunk_count_by_post_id.get(post_id, 0) + 1

        rows.append(
            {
                "post_id": post_id,
                "chunk_index": metadata.get("chunk_index"),
                "preview": _preview_text(str(raw_content)),
                "chunk_id": chunk_id,
                "length": chunk_length,
                "warning": " ⚠️" if chunk_length > 1000 else "",
            }
        )

    rows.sort(
        key=lambda item: (
            item["post_id"] is None,
            item["post_id"] or 0,
            item["chunk_index"] is None,
            item["chunk_index"] or 0,
        )
    )

    print(f"총 청크 개수: {len(rows)}")

    if not rows:
        print("저장된 청크가 없습니다.")
        return

    for row in rows:
        print(
            f"- post_id={row['post_id']}, chunk_index={row['chunk_index']}, "
            f"length={row['length']}{row['warning']}, preview={row['preview']}"
        )

    print("\npost_id별 청크 개수 요약")
    for post_id in sorted(chunk_count_by_post_id):
        print(f"- post_id={post_id}: {chunk_count_by_post_id[post_id]}개")


if __name__ == "__main__":
    main()
