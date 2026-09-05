# 임베딩 모델 설정 및 재인덱싱

임베딩 모델은 `EMBEDDING_PROVIDER`로 선택합니다. 기본값은 Gemini이며,
Hugging Face 사용 시 `sentence-transformers` 기반 모델을 사용합니다.

```env
EMBEDDING_PROVIDER=huggingface
HF_MODEL_NAME=BAAI/bge-m3
HF_DEVICE=
HF_BATCH_SIZE=32
CHROMA_COLLECTION_NAME=
```

`CHROMA_COLLECTION_NAME`을 비워 두면 Gemini는 `traceboard_posts`,
Hugging Face BGE-M3는 `traceboard_posts_hf_bge_m3` 컬렉션을 사용합니다.
모델별 컬렉션은 같은 `backend/chroma_db` 디렉터리 안에서 분리됩니다.

## 전체 게시글 재인덱싱

모델을 변경한 뒤에는 PostgreSQL의 기존 게시글을 새 모델로 다시 임베딩해야 합니다.

```bash
python scripts/reindex_all_posts.py --provider huggingface
```

특정 Hugging Face 모델과 컬렉션을 지정할 수도 있습니다.

```bash
python scripts/reindex_all_posts.py \
  --provider huggingface \
  --model-name BAAI/bge-m3 \
  --collection-name traceboard_posts_hf_bge_m3
```

개별 게시글만 다시 인덱싱할 때는 기존 `POST /api/v1/ai/index-post/{post_id}`
엔드포인트를 사용합니다.
