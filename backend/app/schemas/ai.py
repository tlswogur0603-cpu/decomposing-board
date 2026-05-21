from pydantic import BaseModel, Field

class AIQueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=300, description="사용자가 AI에게 질문")

class SourcePost(BaseModel):
    post_id: int
    title: str | None = Field(default=None, description="AI 답변 생성에 참고한 게시글 제목")

class AIQueryResponse(BaseModel):
    answer: str
    sources: list[SourcePost]

class PostIndexResponse(BaseModel):
    indexed_count: int
    message: str