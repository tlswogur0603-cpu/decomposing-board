# 임베딩 모델 설정 및 재인덱싱

임베딩 모델은 `EMBEDDING_PROVIDER`로 선택합니다. 기본값은 Gemini이며,
Hugging Face 사용 시 `sentence-transformers` 기반 모델을 사용합니다.

## 현재 Base 모델

현재 Hugging Face base 모델은 `BAAI/bge-m3`를 사용합니다.

- 선정 이유: 한국어·다국어 검색을 지원하고 검색용으로 사전 학습된 모델이므로 사내 규정 문서 검색에 적합
- 임베딩 차원: 1024
- 최대 입력 길이: 8192 tokens
- 라이선스: MIT
- 현재 사용 방식: Chroma와 호환되는 dense embedding 검색

## Base 모델 평가 결과

현재 문서 50개, 청크 226개, 평가 질문 100개 기준 BGE-M3 결과입니다.

| 지표 | BGE-M3 |
| --- | ---: |
| Recall@1 | 86% |
| Recall@3 | 96% |
| Recall@5 | 97% |
| MRR | 0.910833 |

Gemini의 기존 결과는 이전 문서·QA셋과 일부 인덱스 상태를 기준으로 측정된 참고값이므로,
BGE-M3 결과와 직접적인 우열 비교에는 사용하지 않습니다.

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
