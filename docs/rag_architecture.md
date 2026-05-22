# RAG Architecture

## 1. Overview
- RAG 기반 게시글 검색 및 질의응답 시스템
- PostgreSQL + Chroma Vector DB + LLM(Gemini) 구조

---

## 2. Indexing Flow (저장 흐름)

### 2.1 게시글 조회
- Repository 계층을 통해 게시글 단건 조회

### 2.2 Document 생성
- page_content: content
- metadata: post_id, title

### 2.3 Vector DB 저장
- Chroma Vector Store 사용
- embedding 후 로컬 DB에 저장

---

## 3. Query Flow (질의응답 흐름)

### 3.1 Similarity Search
- question 기반 유사 Document 검색
- top_k 기준 반환

### 3.2 Context 생성
- Document 리스트 → 문자열 변환

### 3.3 LLM 호출
- context + question 기반 prompt 생성
- Gemini API 호출

### 3.4 Sources 생성
- metadata 기반 (post_id, title)

---

## 4. API

### POST /ai/index-post/{post_id}
- 단건 게시글 인덱싱

### POST /ai/query
- 질의응답 API

---

## 5. Test

- Swagger 기반 테스트 수행
- 인덱싱 → 검색 → 응답 흐름 검증 완료
- Chroma DB 파일 생성 확인

---

## 6. Design Considerations

- Router / Service / Repository 역할 분리
- Document → context 변환 구조
- metadata 기반 source 구성
- 향후 async 및 Background Task 확장 고려