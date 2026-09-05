"""임베딩 모델 생성 및 provider별 설정을 관리한다."""

from functools import lru_cache

from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings


class SentenceTransformerEmbeddings(Embeddings):
    """SentenceTransformer 모델을 LangChain Embeddings 인터페이스로 감싼다."""

    def __init__(
        self,
        model_name: str,
        device: str | None = None,
        batch_size: int = 32,
    ) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "Hugging Face 임베딩을 사용하려면 sentence-transformers를 설치하세요."
            ) from exc

        self.model_name = model_name
        self.batch_size = batch_size
        self.model = SentenceTransformer(model_name, device=device)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embedding.tolist()


@lru_cache(maxsize=1)
def get_embedding_model() -> Embeddings:
    provider = settings.EMBEDDING_PROVIDER.strip().lower()

    if provider == "gemini":
        if not settings.GEMINI_API_KEY:
            raise ValueError("Gemini 임베딩을 사용하려면 GEMINI_API_KEY가 필요합니다.")
        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.GEMINI_API_KEY,
        )

    if provider in {"hf", "huggingface", "sentence-transformers"}:
        return SentenceTransformerEmbeddings(
            model_name=settings.HF_MODEL_NAME,
            device=settings.HF_DEVICE or None,
            batch_size=settings.HF_BATCH_SIZE,
        )

    raise ValueError(
        "지원하지 않는 EMBEDDING_PROVIDER입니다. "
        "gemini 또는 huggingface를 사용하세요."
    )
