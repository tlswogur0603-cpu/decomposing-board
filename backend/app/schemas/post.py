# 요청과 응답데이터 규격을 정의하고 검사하는 코드를 생성해야함.
# Pydantic(BaseModel) 라이브러리를 사용하여 Class를 생성해야함.
# 사용자의 요청 즉 입력 값을 검증하는 클래스 Class PostCreate(BaseModel) -> title, content 생성
# title, content 모두 stirng으로 받을 것임 title은 비어있어도 상관없음 content는 필수로 있어야함 
# title은 최대 30자 까지 허용 content는 최대 300자 까지 허용
# 응답 데이터 규격 정의 Class PostRead(BaseModel) 
# -> id(게시글 id), title, cotent, author_id(사용자 id) 반환 
from pydantic import BaseModel, Field
from typing import Optional

class PostCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=30)
    content: str = Field(..., min_length=1, max_length=300)

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int

    class Config:
        from_attributes = True

# 기본 스키마 요청 응답 데이터 규격 정의