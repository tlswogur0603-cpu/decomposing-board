# API Specification - TraceBoard AI

## Base URL

`/api/v1`

---

## 1. 게시글 생성 (Create Post)

**POST** `/posts`

### 설명
- 새 게시글 생성

### Request Body
​
{
"title": "게시글 제목",
"content": "게시글 내용"
}

### Response
​
{
"id": 1,
"title": "게시글 제목",
"content": "게시글 내용",
"author_id": 1,
"created_at": "2026-05-15T12:00:00"
}

### Status Codes
- `201 Created`
- `422 Validation Error`

---

## 2. 전체 게시글 조회 (Get All Posts)

**GET** `/posts`

### 설명
- 전체 게시글 최신순 조회

### Response
​
[
{
"id": 1,
"title": "게시글 제목",
"content": "게시글 내용",
"author_id": 1,
"created_at": "2026-05-15T12:00:00"
}
]

### Status Codes
- `200 OK`

---

## 3. 단일 게시글 조회 (Get Post Detail)

**GET** `/posts/{post_id}`

### 설명
- 특정 게시글 조회

### Path Parameter
​
post_id: int

### Response
​
{
"id": 1,
"title": "게시글 제목",
"content": "게시글 내용",
"author_id": 1,
"created_at": "2026-05-15T12:00:00"
}

### Status Codes
- `200 OK`
- `404 Not Found`

---

## 4. 게시글 수정 (Update Post)

**PUT** `/posts/{post_id}`

### 설명
- 특정 게시글 전체 수정

### Request Body
​
{
"title": "수정된 제목",
"content": "수정된 내용"
}

### Response
​
{
"id": 1,
"title": "수정된 제목",
"content": "수정된 내용",
"author_id": 1,
"created_at": "2026-05-15T12:00:00"
}

### Status Codes
- `200 OK`
- `404 Not Found`
- `422 Validation Error`

---

## 5. 게시글 삭제 (Delete Post)

**DELETE** `/posts/{post_id}`

### 설명
- 특정 게시글 삭제

### Response
​
{
"message": "게시글이 삭제되었습니다."
}

### Status Codes
- `200 OK`
- `404 Not Found`

---

## 데이터 스키마

### PostCreate
​
{
"title": "string | null (max 30)",
"content": "string (1~300)"
}

### PostUpdate
​
{
"title": "string | null (max 30)",
"content": "string (1~300)"
}

### PostRead
​
{
"id": "int",
"title": "string | null",
"content": "string",
"author_id": "int",
"created_at": "datetime"
}

---

## 공통 아키텍처 흐름

​
Client Request
→ FastAPI Router
→ Pydantic Validation
→ Service Layer
→ Repository Layer
→ PostgreSQL (Supabase)
→ Response

---

## 향후 확장 예정 API

- `GET /posts/search`
- `GET /posts?page=`
- `POST /documents/upload`
- `POST /ai/query`
- `GET /ai/history`