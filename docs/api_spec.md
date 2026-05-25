# API Specification - TraceBoard AI

## Base URL

`/api/v1`

---

## 1. 게시글 생성 (Create Post)

**POST** `/posts`

### 설명
- 새 게시글 생성

### Request Body

```json
{
"title": "게시글 제목",
"content": "게시글 내용"
}
```

### Response
​
```json
{
"id": 1,
"title": "게시글 제목",
"content": "게시글 내용",
"author_id": 1,
"created_at": "2026-05-15T12:00:00"
}
```

### Status Codes
- `201 Created`
- `422 Validation Error`

---

## 2. 전체 게시글 조회 (Get All Posts)

**GET** `/posts`

### 설명
- 게시글 목록을 최신순으로 조회
- page, limit query parameter를 사용하여 페이지 단위로 조회

### Query Parameters

| Name | Type | Required | Default | Validation | Description |
| --- | --- | --- | --- | --- | --- |
| `page` | int | No | `1` | `page >= 1` | 조회할 페이지 번호 |
| `limit` | int | No | `3` | `1 <= limit <= 10` | 한 페이지에 조회할 게시글 수 |

### Request Example

`GET /posts?page=1&limit=3`

### Response

```json
{
"total_count": 11,
"total_pages": 4,
"current_page": 1,
"limit": 3,
"items": [
{
"id": 12,
"title": "계속",
"content": "도전",
"author_id": 1,
"created_at": "2026-05-16T11:36:28.298999Z"
},
{
"id": 11,
"title": "날씨",
"content": "더움",
"author_id": 1,
"created_at": "2026-05-16T11:36:13.973500Z"
}
]
}
```

### Status Codes
- `200 OK`
- `422 Validation Error`

### Notes
- 기본 요청 `GET /posts`는 `page=1`, `limit=3`으로 처리된다.
- 정렬 기준은 `created_at DESC`이다.
- `page=0`, `limit=0`, `limit=11`처럼 허용 범위를 벗어난 값은 검증 단계에서 거부된다.

---

## 3. 게시글 검색 (Search Posts)

**GET** `/posts/search`

### 설명
- 게시글 제목 또는 본문에 검색어가 포함된 게시글 목록 조회
- 검색 결과는 `created_at` 기준 최신순으로 정렬
- 검색어가 비어 있거나 검색 결과가 없으면 빈 리스트 반환

### Query Parameters

| Name | Type | Required | Default | Validation | Description |
| --- | --- | --- | --- | --- | --- |
| `q` | string | No | `""` | `max_length=50` | 검색할 키워드 |

### Request Example

`GET /posts/search?q=FastAPI`

### Response

```json
[
{
"id": 1,
"title": "FastAPI 학습",
"content": "FastAPI Query Parameter를 학습했습니다.",
"author_id": 1,
"created_at": "2026-05-15T12:00:00"
}
]
```

### Empty Response

```json
[
]
```

### Status Codes
- `200 OK`
- `422 Validation Error`

### Notes
- `q` 값은 앞뒤 공백을 제거한 뒤 검색에 사용된다.
- `title` 또는 `content`에 검색어가 포함되면 결과에 포함된다.
- `ILIKE`를 사용하여 대소문자를 구분하지 않는 검색을 수행한다.
- `GET /posts/search`처럼 검색어가 없으면 빈 리스트를 반환한다.

---

## 4. 단일 게시글 조회 (Get Post Detail)

**GET** `/posts/{post_id}`

### 설명
- 특정 게시글 조회

### Path Parameter
​
post_id: int

### Response
​
```json
{
"id": 1,
"title": "게시글 제목",
"content": "게시글 내용",
"author_id": 1,
"created_at": "2026-05-15T12:00:00"
}
```

### Status Codes
- `200 OK`
- `404 Not Found`

---

## 5. 게시글 수정 (Update Post)

**PUT** `/posts/{post_id}`

### 설명
- 특정 게시글 전체 수정

### Request Body
​
```json
{
"title": "수정된 제목",
"content": "수정된 내용"
}
```

### Response
​
```json
{
"id": 1,
"title": "수정된 제목",
"content": "수정된 내용",
"author_id": 1,
"created_at": "2026-05-15T12:00:00"
}
```

### Status Codes
- `200 OK`
- `404 Not Found`
- `422 Validation Error`

---

## 6. 게시글 삭제 (Delete Post)

**DELETE** `/posts/{post_id}`

### 설명
- 특정 게시글 삭제

### Response
​
```json
{
"message": "게시글이 삭제되었습니다."
}
```

### Status Codes
- `200 OK`
- `404 Not Found`

---

## 데이터 스키마

### PostCreate
​
```json
{
"title": "string | null (max 30)",
"content": "string (1~300)"
}
```

### PostUpdate
​
```json
{
"title": "string | null (max 30)",
"content": "string (1~300)"
}
```

### PostRead

```json
{
"id": "int",
"title": "string | null",
"content": "string",
"author_id": "int",
"created_at": "datetime"
}
```

---

## 공통 아키텍처 흐름

```mermaid
graph TD
    A[Client Request] --> B[FastAPI Router (Pydantic)]
    B --> C[Service Layer (Business)]
    C --> D[Repository Layer (DB Abstraction)]
    D --> E[PostgreSQL (Source of Truth)]
    D --> F[Chroma DB (Vector Storage)]
    E --> G[Response]
    F --> G
```

---

## 향후 확장 예정 API

- **[Implemented]** `GET /posts/search`
- **[Implemented]** `GET /posts?page=`
- **[Implemented]** `POST /ai/query`
- **[Planned]** `POST /documents/upload`
- **[Planned]** `GET /ai/history`
- **[Planned]** `DELETE /ai/index/{post_id}`

---

## 7. RAG 인덱싱 (Index Post)

**POST** `/ai/index-post/{post_id}`

### 설명
- **데이터 통합**: PostgreSQL에 저장된 특정 게시글(ID 기반)을 조회하여 임베딩한 후 Vector DB(Chroma)에 동기화합니다.
- **자동화 설계**: 게시글 생성(`POST /posts`) 시 서버 내부에서 Background Task를 통해 이 로직이 자동으로 호출됩니다.
- **수동 활용**: 데이터 정합성 보정이 필요하거나, 특정 게시글을 강제로 재인덱싱할 때 사용합니다.

### Path Parameter
- `post_id`: (int) PostgreSQL에 저장된 게시글 고유 ID

### Response
```json
{
  "indexed_count": 1,
  "message": "게시글 인덱싱이 완료되었습니다."
}
```

### Status Codes
- `200 OK`
- `404 Not Found`

---

## 8. RAG 질의응답 (Query)

**POST** `/ai/query`

### 설명
- **RAG(Retrieval-Augmented Generation)** 메커니즘을 기반으로 사용자의 질문에 답변을 생성합니다.
- 사용자의 질문과 의미적으로 유사한 게시글을 Vector DB에서 검색하고, 추출된 정보를 바탕으로 LLM(Gemini)이 근거 있는 답변을 도출합니다.

### Request Body
```json
{
  "query": "사용자 질문 내용 (예: 'FastAPI 비동기 처리 방법 알려줘')"
}
```

### Response
```json
{
  "answer": "AI가 생성한 답변",
  "sources": [
    {
      "post_id": 1,
      "title": "관련 문서 제목"
    }
  ]
}
```

### Status Codes
- `200 OK`
- `422 Validation Error`