from pydantic import BaseModel, Field

class AIQueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=300, description="사용자가 AI에게 질문")

class SourcePost(BaseModel):
    post_id: int
    title: str | None = Field(default=None, description="AI 답변 생성에 참고한 게시글 제목")
    chunk_index: int | None = Field(default=None, description="참고한 청크의 0-based 인덱스")
    chunk_count: int | None = Field(default=None, description="해당 게시글의 전체 청크 수")

class AIQueryResponse(BaseModel):
    answer: str
    sources: list[SourcePost]

class PostIndexResponse(BaseModel):
    indexed_count: int
    message: str
