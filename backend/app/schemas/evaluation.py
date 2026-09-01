from pydantic import BaseModel, ConfigDict, Field


class QAEvaluationItem(BaseModel):
    question: str = Field(..., min_length=2, max_length=300, description="평가용 질문")
    relevant_post_ids: list[int] = Field(
        ...,
        min_length=1,
        description="정답으로 연결되는 게시글 ID 목록",
    )

    model_config = ConfigDict(extra="ignore")
