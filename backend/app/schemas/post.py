# 게시글 요청/응답 스키마 정의
# PostCreate는 요청 검증, PostRead는 응답 담당.

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class PostCreate(BaseModel):
    title: str | None = Field(None, max_length=30)
    content: str = Field(..., min_length=1, max_length=300)

class PostRead(BaseModel):
    id: int
    title: str | None
    content: str
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# 기본 스키마 요청 응답 데이터 규격 정의