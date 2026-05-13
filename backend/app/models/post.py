# 게시글(posts) 테이블을 표현하는 SQLAlchemy ORM 모델
# Supabase에 생성한 posts 테이블 컬럼 구조와 맞춤.

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())