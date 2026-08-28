# Embedding Service는 텍스트를 벡터로 변환할 수 있는 임베딩 모델 객체를 생성하고 반환합니다.

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings


_embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=settings.GEMINI_API_KEY,
)


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    return _embedding_model