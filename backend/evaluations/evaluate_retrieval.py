"""QA 평가셋으로 벡터 검색의 Recall@K와 MRR을 계산한다.

실행 예:
    python backend/evaluations/evaluate_retrieval.py --top-k 1,3,5
    python backend/evaluations/evaluate_retrieval.py --output evaluation_results.csv

검색은 API를 거치지 않고 기존 vector_repository를 직접 호출한다.
다른 임베딩 모델을 평가할 때는 ``evaluate_qa_set``에 해당 모델을 사용하는
비동기 search_fn을 주입하면 동일한 평가 로직을 재사용할 수 있다.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections.abc import Awaitable, Callable, Sequence
from pathlib import Path
from typing import Any

import pandas as pd
from langchain_core.documents import Document

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.repositories.vector_repository import search_similar_posts
from app.schemas.evaluation import QAEvaluationItem
from app.utils.qa_loader import QA_SET_PATH, load_qa_set

SearchFunction = Callable[[str, int], Awaitable[list[Document]]]


def _unique_post_ids(documents: Sequence[Document]) -> list[int]:
    """검색된 청크를 게시글 ID 목록으로 변환하고 중복을 제거한다."""
    post_ids: list[int] = []
    seen: set[int] = set()
    for document in documents:
        raw_post_id = document.metadata.get("post_id")
        try:
            post_id = int(raw_post_id)
        except (TypeError, ValueError):
            continue
        if post_id not in seen:
            seen.add(post_id)
            post_ids.append(post_id)
    return post_ids


def _first_relevant_rank(
    retrieved_post_ids: Sequence[int],
    relevant_post_ids: Sequence[int],
) -> int | None:
    relevant = set(relevant_post_ids)
    for rank, post_id in enumerate(retrieved_post_ids, start=1):
        if post_id in relevant:
            return rank
    return None


def evaluate_qa_set(
    qa_items: Sequence[QAEvaluationItem],
    *,
    top_k_values: Sequence[int] = (1, 3, 5),
    search_fn: SearchFunction = search_similar_posts,
    model_name: str = "gemini",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """QA별 상세 결과와 전체 지표 요약 DataFrame을 반환한다."""
    normalized_k = sorted({int(k) for k in top_k_values if int(k) > 0})
    if not normalized_k:
        raise ValueError("top_k_values에는 1 이상의 값이 하나 이상 필요합니다.")

    async def run_searches() -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        max_k = normalized_k[-1]
        for item in qa_items:
            documents = await search_fn(item.question, max_k)
            retrieved_post_ids = _unique_post_ids(documents)
            rank = _first_relevant_rank(
                retrieved_post_ids,
                item.relevant_post_ids,
            )
            row: dict[str, Any] = {
                "model": model_name,
                "question": item.question,
                "relevant_post_ids": list(item.relevant_post_ids),
                "retrieved_post_ids": retrieved_post_ids,
                "first_relevant_rank": rank,
                "reciprocal_rank": 1 / rank if rank is not None else 0.0,
            }
            for k in normalized_k:
                row[f"recall_at_{k}"] = int(
                    rank is not None and rank <= k
                )
            rows.append(row)
        return rows

    detail_df = pd.DataFrame(asyncio.run(run_searches()))
    summary: dict[str, Any] = {
        "model": model_name,
        "query_count": len(detail_df),
        "mrr": (
            float(detail_df["reciprocal_rank"].mean())
            if not detail_df.empty
            else 0.0
        ),
    }
    for k in normalized_k:
        column = f"recall_at_{k}"
        summary[column] = (
            float(detail_df[column].mean()) if not detail_df.empty else 0.0
        )
    summary_df = pd.DataFrame([summary])
    return detail_df, summary_df


def _parse_top_k(value: str) -> list[int]:
    try:
        values = [int(item.strip()) for item in value.split(",")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("K는 쉼표로 구분한 정수여야 합니다.") from exc
    if not values or any(item <= 0 for item in values):
        raise argparse.ArgumentTypeError("K는 1 이상의 정수여야 합니다.")
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description="QA 기반 벡터 검색 성능 평가")
    parser.add_argument(
        "--qa-path",
        type=Path,
        default=QA_SET_PATH,
        help=f"QA JSON 경로 (기본값: {QA_SET_PATH})",
    )
    parser.add_argument(
        "--top-k",
        type=_parse_top_k,
        default=[1, 3, 5],
        help="Recall@K에 사용할 K 목록 (예: 1,3,5)",
    )
    parser.add_argument(
        "--model-name",
        default="gemini",
        help="결과에 표시할 임베딩 모델 이름",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="상세 결과를 저장할 CSV 경로 (선택)",
    )
    args = parser.parse_args()

    qa_items = load_qa_set(args.qa_path)
    detail_df, summary_df = evaluate_qa_set(
        qa_items,
        top_k_values=args.top_k,
        model_name=args.model_name,
    )

    print(f"QA 파일: {args.qa_path}")
    print(f"임베딩 모델: {args.model_name}")
    print("\n전체 평가 지표")
    print(summary_df.to_string(index=False))
    print("\n질문별 평가 결과")
    print(detail_df.to_string(index=False))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        detail_df.to_csv(args.output, index=False, encoding="utf-8-sig")
        print(f"\n상세 결과 저장: {args.output}")


if __name__ == "__main__":
    main()
