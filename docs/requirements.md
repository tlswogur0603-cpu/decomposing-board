# Requirements Specification - TraceBoard AI

## 1. 프로젝트 목적
TraceBoard AI는 구조적 게시판 시스템을 기반으로,
향후 AI 및 RAG 기술을 통합하여
개인 및 조직의 지식 데이터를 저장·검색·활용할 수 있는
AI 기반 지식 관리 플랫폼 구축을 목표로 한다.

---

## 2. 현재 기능 요구사항 (Phase 1 - MVP)

### 2.1 게시글 관리 기능
- 사용자는 게시글을 생성할 수 있어야 한다.
- 사용자는 전체 게시글 목록을 조회할 수 있어야 한다.
- 사용자는 특정 게시글 단건 조회가 가능해야 한다.
- 사용자는 게시글을 수정할 수 있어야 한다.
- 사용자는 게시글을 삭제할 수 있어야 한다.

---

### 2.2 데이터 검증
- title:
  - 선택 입력
  - 최대 30자
- content:
  - 필수 입력
  - 최소 1자
  - 최대 300자

---

### 2.3 시스템 구조 요구사항
- Router / Service / Repository 구조를 유지해야 한다.
- DB 접근 로직과 비즈니스 로직은 분리되어야 한다.
- FastAPI Depends 기반 DB 세션 주입 구조를 사용해야 한다.
- Pydantic 기반 요청/응답 검증을 적용해야 한다.

---

### 2.4 데이터베이스 요구사항
- PostgreSQL(Supabase) 사용
- SQLAlchemy ORM 사용
- created_at 자동 생성
- author_id 추후 인증 시스템 연동 고려

---

## 3. 향후 기능 요구사항 (Phase 2+)

### 3.1 게시판 고도화
- Pagination
- 검색 기능
- 카테고리 분류
- 사용자 인증(JWT)
- 권한 관리

---

### 3.2 문서 관리
- PDF 업로드
- Markdown 업로드
- 텍스트 추출
- 문서 메타데이터 저장

---

### 3.3 AI / RAG
- 문서 Chunking
- Embedding 생성
- Vector DB 저장
- 문맥 기반 검색
- LangChain 오케스트레이션
- 질문 응답
- AI 요약
- 관련 문서 추천

---

### 3.4 모델 확장성
- Gemini
- OpenAI
- Ollama(Local LLM)

---

## 4. 비기능 요구사항

### 성능
- RESTful API 구조 유지
- 빠른 CRUD 응답 속도
- 향후 비동기 확장 가능 구조

---

### 유지보수성
- Layered Architecture
- 코드 재사용성
- 테스트 용이성
- 환경변수 기반 설정 분리

---

### 보안
- 환경변수(.env) 분리
- DB URL 보호
- 향후 인증/인가 확장 가능 구조

---

## 5. 개발 우선순위

### 우선
- CRUD 안정화
- 문서화
- Pagination
- 검색

### 이후
- RAG
- AI 질의응답
- 인증
- 협업 기능

---

## 6. 성공 기준
- CRUD API 정상 동작
- Supabase 연동 안정화
- 구조적 백엔드 아키텍처 확보
- AI 확장 가능 구조 확보