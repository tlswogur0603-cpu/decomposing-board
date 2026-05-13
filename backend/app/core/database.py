# DB작업을 하기 위한 공통 준비 파일 
# config.py의 settings.DATABASE_URL을 사용해 DB 연결 기반(engine)을 만든다.
# 요청마다 사용할 DB 세션을 만들 수 있도록 SessionLocal을 구성한다.
# SQLAlchemy 모델들이 상속할 Base를 정의한다.
# FastAPI Depends에서 사용할 get_db 함수로 세션 생성/종료를 관리한다.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()