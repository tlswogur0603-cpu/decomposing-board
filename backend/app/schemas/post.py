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

class PostUpdate(BaseModel):
    title: str | None = Field(None, max_length=30)
    content: str = Field(..., min_length=1, max_length=300)

class PostPaginationResponse(BaseModel):
    total_count: int      # 전체 게시글 수
    total_pages: int      # 총 페이지 수
    current_page: int     # 현재 페이지
    limit: int            # 페이지당 개수
    items: list[PostRead] # 실제 게시글 데이터 리스트