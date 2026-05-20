# Architecture Design

## 1. 개요 (Architecture Philosophy)
TraceBoard AI는 **"변하는 것과 변하지 않는 것의 분리"**를 핵심 원칙으로 설계되었습니다. 
현재는 데이터의 무결성을 보장하는 RDB 기반의 웹 서비스 구조를 취하고 있으며, 향후 AI 엔진(LLM)이나 벡터 데이터베이스의 변화에 유연하게 대응할 수 있는 구조를 지향합니다.

---

## 2. 현재 운영 구조 (Current Implementation)
현재 시스템은 전형적인 **Layered Architecture**를 따르며, 동기/비동기 처리를 효율적으로 관리합니다.

### **Data Flow: CRUD Pipeline**
1.  **API Layer (`api/v1/`)**: 클라이언트 요청 수신 및 `Pydantic` 스키마를 통한 유효성 검증.
2.  **Service Layer (`services/`)**: 비즈니스 정책 수행. (현재는 CRUD 로직 중계 및 기초 가공)
3.  **Repository Layer (`repositories/`)**: `SQLAlchemy`를 통한 DB 추상화. 원시 쿼리와 비즈니스 로직을 분리.
4.  **Database**: `PostgreSQL (Supabase)`에 영구 저장.

---

## 3. AI 확장 설계 (Planned AI Pipeline)

향후 도입될 AI 기능은 기존 `Service Layer`를 확장하거나 별도의 AI 전용 서비스 모듈을 통해 통합될 예정입니다.  
TraceBoard AI의 AI 기능은 단순 LLM 호출이 아니라, 사용자가 작성한 게시글과 향후 업로드될 문서를 기반으로 답변을 생성하는 **RAG(Retrieval-Augmented Generation)** 구조를 지향합니다.

### 3.1 RAG 대상 데이터

#### MVP 범위
- 현재 MVP에서는 사용자가 작성한 `posts` 데이터를 RAG 대상으로 사용합니다.
- 게시글의 `title`과 `content`를 하나의 문서 단위로 보고 임베딩합니다.
- 게시글 하나가 비교적 짧은 의미 단위이므로, 초기 MVP에서는 별도 chunking 없이 게시글 단위로 Vector DB에 저장합니다.

#### 향후 확장 범위
- PDF, Markdown, Text 파일 업로드 기능을 추가합니다.
- 긴 문서는 Text Extraction 이후 chunking을 적용하여 작은 검색 단위로 분리합니다.
- 각 chunk를 임베딩하여 Vector DB에 저장하고, 질문과 가장 유사한 chunk를 검색해 LLM context로 전달합니다.

---

### 3.2 Knowledge Ingestion Flow

#### MVP: 게시글 기반 인덱싱
1. 사용자가 게시글을 생성합니다.
2. 게시글 원본 데이터는 PostgreSQL(Supabase)의 `posts` 테이블에 저장됩니다.
3. 게시글의 `title`과 `content`를 임베딩 대상으로 구성합니다.
4. 임베딩 모델을 통해 벡터를 생성합니다.
5. 생성된 벡터와 metadata를 Vector DB에 저장합니다.

#### Vector DB Metadata
Vector DB에는 유사도 검색 이후 LLM context와 출처 정보를 구성할 수 있도록 metadata를 함께 저장합니다.

- `post_id`: PostgreSQL 원본 게시글 ID
- `title`: 게시글 제목
- `content`: 게시글 본문

PostgreSQL은 원본 데이터 저장소 역할을 담당하고, Vector DB는 의미 기반 검색을 위한 검색 최적화 저장소 역할을 담당합니다.

---

### 3.3 Planned RAG Query Flow

1. 사용자가 `POST /ai/query` API로 질문을 전달합니다.
2. 서버는 사용자의 질문을 임베딩합니다.
3. Vector DB에서 질문 벡터와 유사도가 높은 게시글 벡터를 검색합니다.
4. 검색 결과의 metadata에서 `title`, `content`, `post_id`를 가져옵니다.
5. 선택된 게시글 내용을 LLM의 context로 전달합니다.
6. LLM은 context를 기반으로 답변을 생성합니다.
7. 서버는 AI 답변과 참고한 게시글 목록을 함께 반환합니다.

---

### 3.4 Planned API Structure

#### `POST /ai/index-posts`
- PostgreSQL에 저장된 게시글을 읽어 임베딩합니다.
- 임베딩 결과를 Vector DB에 저장합니다.
- 초기 MVP에서는 수동 인덱싱 API로 사용하고, 향후 게시글 생성 시 자동 인덱싱 또는 background task 구조로 확장할 수 있습니다.

#### `POST /ai/query`
- 사용자의 질문을 입력받습니다.
- Vector DB에서 관련 게시글을 검색합니다.
- 검색된 게시글을 context로 구성하여 LLM에 전달합니다.
- 최종 답변과 출처 목록을 반환합니다.

#### `POST /documents/upload` *(Phase 2)*
- 문서 업로드 API입니다.
- 문서 텍스트 추출, chunking, embedding, Vector DB 저장 흐름으로 확장할 예정입니다.

---

### 3.5 Component Responsibility

- **AI Router (`api/v1/ai.py`)**
  - AI 관련 요청 진입점
  - 요청/응답 스키마 검증
  - RAG Service 호출

- **RAG Service (`services/rag_service.py`)**
  - 질문 처리 흐름 총괄
  - Retriever 호출
  - LLM context 구성
  - AI 답변 및 출처 응답 조립

- **Embedding Service (`services/embedding_service.py`)**
  - 게시글 또는 질문 텍스트를 임베딩 벡터로 변환

- **Vector Repository (`repositories/vector_repository.py`)**
  - Vector DB 저장
  - Similarity Search 수행
  - 검색 결과 metadata 반환

- **Post Repository (`repositories/post_repository.py`)**
  - PostgreSQL에 저장된 게시글 원본 데이터 조회

---

### 3.6 Vector DB Selection

MVP 단계에서는 로컬 개발과 빠른 검증이 쉬운 `Chroma`를 우선 고려합니다.

- **Chroma**
  - 로컬 개발 및 MVP 검증에 적합
  - LangChain 연동이 비교적 단순함

향후 운영 환경 또는 공고 요구사항 대응을 위해 다음 Vector DB도 확장 후보로 고려합니다.

- **Pinecone**
  - 클라우드 기반 Vector DB
  - 운영 환경 확장성에 강점

- **LanceDB**
  - 로컬/파일 기반 벡터 저장에 적합
  - 경량 AI 검색 시스템에 활용 가능

---

## 4. 확장성을 고려한 설계 포인트
- **Repository Pattern**: 현재는 PostgreSQL을 사용 중이나, 향후 Vector DB(Chroma 등)와의 하이브리드 운영을 위해 데이터 접근 계층을 추상화하였습니다.
- **Dependency Injection**: FastAPI의 `Depends`를 활용하여 DB 세션 및 서비스 객체를 주입함으로써 테스트 용이성과 결합도를 낮췄습니다.
- **Service Decoupling**: AI 질의응답 로직을 서비스 레이어 내 별도 컴포넌트로 분리하여, 일반 게시판 기능과 AI 기능이 서로 간섭 없이 확장될 수 있도록 설계했습니다.

---

## 5. 동기/비동기 확장 고려사항 (Sync/Async Scalability Consideration)

- 현재 TraceBoard AI는 CRUD, Pagination, Search 중심의 MVP 구조로 비교적 짧은 DB I/O 작업을 수행합니다.
- 따라서 현재 단계에서는 sync SQLAlchemy 구조가 단순성과 유지보수 측면에서 효율적입니다.
- 단순 Router 계층의 async 전환만으로는 충분하지 않으며, 실제 async 구조 전환 시:
  - Async SQLAlchemy Engine
  - Async DB Driver
  - Router / Service / Repository 전체 체인 전환
이 필요합니다.

### 우선 고려 성능 요소
- 전체 데이터 조회 비용
- COUNT 비용
- OFFSET 증가
- LIKE / ILIKE 검색 비용
- Query 최적화 및 Index 설계

### 향후 async 전환 고려 시점
- 외부 LLM API 호출 증가
- 문서 업로드 및 대용량 처리
- Vector DB 기반 검색
- 동시 사용자 증가