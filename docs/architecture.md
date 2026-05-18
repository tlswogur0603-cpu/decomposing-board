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
향후 도입될 AI 기능은 기존 `Service Layer`를 확장하거나 별도의 AI 전용 모듈을 통해 통합될 예정입니다.

### **Planned: Knowledge Ingestion Flow**
- **Document Processing**: 문서 업로드 -> Text Extraction -> **Recursive Character Chunking**.
- **Vectorization**: `OpenAI/Gemini Embedding` 모델을 통한 벡터화.
- **Storage**: `Vector DB`에 벡터 및 메타데이터 저장.

### **Planned: RAG (Retrieval-Augmented Generation) Flow**
1.  **Retrieve**: 사용자 질문 입력을 임베딩하여 Vector DB에서 관련 문서 추출.
2.  **Augment**: 질문과 추출된 문서를 결합하여 Prompt 구성.
3.  **Generate**: LLM이 제공된 Context를 기반으로 최종 답변 생성.

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