from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.schemas.evaluation import QAEvaluationItem


EVALUATION_DIR = Path(__file__).resolve().parents[2] / "evaluations"
QA_SET_PATH = EVALUATION_DIR / "qa_set.json"


def load_qa_set(path: str | Path | None = None) -> list[QAEvaluationItem]:
    file_path = Path(path) if path is not None else QA_SET_PATH

    with file_path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return _parse_qa_items(raw_data)


def _parse_qa_items(raw_data: Any) -> list[QAEvaluationItem]:
    if isinstance(raw_data, list):
        items = raw_data
    elif isinstance(raw_data, dict):
        items = raw_data.get("items", [])
    else:
        raise ValueError("qa_set.json은 배열 또는 items를 가진 객체 형태여야 합니다.")

    if not isinstance(items, list):
        raise ValueError("qa_set.json의 items는 배열 형태여야 합니다.")

    return [QAEvaluationItem.model_validate(item) for item in items]
