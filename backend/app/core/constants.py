from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

CHROMA_COLLECTION_NAME = "traceboard_posts"
CHROMA_PERSIST_DIRECTORY = PROJECT_ROOT / "backend" / "chroma_db"

POST_CONTENT_MAX_LENGTH = 10_000
POST_CHUNK_SIZE = 500
POST_CHUNK_OVERLAP = 50
