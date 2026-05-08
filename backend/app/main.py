# FastAPI 프레임워크를 import해
# app/api/v1/posts.py파일에서 router를 가져오고 이것을 posts_router라고 부를거야.
# posts_router를 포함해서 FastAPI서버를 만들어줘 접두사는 api/v1으로 지정해.

from fastapi import FastAPI
from app.api.v1.posts import router as posts_router

app = FastAPI()

app.include_router(posts_router, prefix="/api/v1")