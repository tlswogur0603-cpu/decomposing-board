from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
for import_path in (PROJECT_ROOT, BACKEND_ROOT):
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))

from backend.app.utils.qa_loader import load_qa_set


def main() -> None:
    qa_set = load_qa_set()

    print(f"총 QA 개수: {len(qa_set)}")

    if not qa_set:
        print("저장된 QA가 없습니다.")
        return

    for item in qa_set:
        post_ids = ", ".join(str(post_id) for post_id in item.relevant_post_ids)
        print(f"- question={item.question} | relevant_post_ids=[{post_ids}]")


if __name__ == "__main__":
    main()
