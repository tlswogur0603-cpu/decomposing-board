from __future__ import annotations

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
