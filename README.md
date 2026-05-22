# TraceBoard AI

> **단순한 기록을 넘어, AI 기반의 지능형 지식 관리 플랫폼으로.**
>
> TraceBoard AI는 Layered Architecture 기반의 게시판 시스템 위에  
> **RAG(Retrieval-Augmented Generation)** 파이프라인을 구축하여  
> 저장된 데이터를 기반으로 AI 질의응답을 제공하는 백엔드 프로젝트입니다.

---

## Project Overview

TraceBoard AI는 흩어진 메모, 문서, 기록들을 한곳에 모으고  
AI가 이를 기반으로 맥락에 맞는 답변을 제공하는 플랫폼입니다.

현재 프로젝트는 다음 기능을 포함합니다:

- 게시글 CRUD API
- PostgreSQL 기반 데이터 저장
- Vector DB(Chroma)를 활용한 임베딩 저장
- RAG 기반 질의응답 API 제공

---

## Tech Stack

### Backend

- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic v2
- **Architecture**: Layered Architecture (Router - Service - Repository)

### AI & Data (Implemented)

- **Vector DB**: Chroma
- **Embedding**: (사용 모델 명시 가능)
- **LLM**: Gemini API
- **Pipeline**: RAG (Retrieval-Augmented Generation)

---

## Development Status

### 1. Current Implementation (MVP)

- ✅ Layered Architecture 설계 및 구현
- ✅ PostgreSQL 연동 (Supabase)
- ✅ 게시글 CRUD API
- ✅ RAG 인덱싱 API (`/ai/index-post/{post_id}`)
- ✅ Vector DB 저장 (Chroma)
- ✅ RAG 기반 질의응답 API (`/ai/query`)
- ✅ LLM 연동 (Gemini)

### 2. Future Roadmap

- ⬜ Async 구조 전환 (비동기 처리 최적화)
- ⬜ Background Task (자동 인덱싱)
- ⬜ 검색 고도화 (필터링, 정렬)
- ⬜ Vector DB 확장 (FAISS, Pinecone)
- ⬜ Local LLM 연동 (Ollama)

---

## Architecture

👉 자세한 구조는 아래 문서를 참고하세요:

- `docs/architecture.md`
- `docs/rag_architecture.md`

---

## RAG Pipeline Overview

### 1. Indexing (저장 흐름)

1. PostgreSQL에서 게시글 조회
2. Embedding 생성
3. Chroma Vector DB 저장
4. metadata (post_id, title, content) 함께 저장

### 2. Query (질의응답 흐름)

1. 사용자 질문 입력
2. Vector DB에서 유사 문서 검색 (similarity search)
3. Document → context 변환
4. LLM 호출 (context + question)
5. 답변 + sources 반환

---

## API Specification

### 🔹 RAG Indexing

​
POST /ai/index-post/{post_id}

### 🔹 RAG Query

​
POST /ai/query

👉 자세한 요청/응답은 `docs/api_spec.md` 참고

---

## Folder Structure

​
backend/app/
├── api/v1/          # API 엔드포인트
├── core/            # 설정 및 DB 연결
├── models/          # DB 모델
├── schemas/         # 요청/응답 스키마
├── repositories/    # 데이터 접근 계층
├── services/        # 비즈니스 로직 (RAG 포함)
└── main.py          # 앱 진입점

---

## Key Design

- **Layered Architecture**
  - Router: 요청/응답 처리
  - Service: 비즈니스 로직
  - Repository: DB 접근

- **RAG 구조**
  - 데이터 → 벡터화 → 검색 → LLM 응답

---

## Notes

- 현재 구조는 **Async 확장을 고려한 설계**
- RAG 파이프라인은 MVP 수준으로 구현 완료
- 향후 대용량 처리 및 성능 개선 예정
​