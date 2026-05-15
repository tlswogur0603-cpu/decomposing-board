# TraceBoard AI

> **단순한 기록을 넘어, AI 기반의 지능형 지식 관리 플랫폼으로.**
> TraceBoard AI는 현재 견고한 Layered Architecture 기반의 게시판 MVP를 구축 완료하였으며, 향후 RAG(Retrieval-Augmented Generation) 기술을 통합하여 개인 및 조직의 지식 자산을 지능적으로 활용하는 플랫폼을 지향합니다.

---

## Project Overview
TraceBoard AI는 흩어진 메모, 문서, 기록들을 한곳에 모으고 AI가 이를 학습하여 맥락에 맞는 답변을 제공하는 플랫폼입니다. 
현재 **Phase 1: 안정적인 Backend 인프라 및 CRUD API** 구현 단계에 있으며, 구조적 유연성을 확보하여 AI 모듈 확장을 준비하고 있습니다.

## Tech Stack
### **Backend (Current)**
- **Framework**: FastAPI (Async-ready architecture)
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic v2
- **Architecture**: Layered Architecture (Router - Service - Repository)

### **AI & Data (Planned)**
- **Orchestration**: LangChain
- **Vector DB**: Chroma / FAISS / Pinecone
- **LLM**: Gemini / OpenAI / Ollama (Local)

---

## Development Status

### **1. Current Implementation (MVP Phase)**
현재 프로젝트는 비즈니스 로직과 데이터 접근 계층이 엄격히 분리된 **구조적 MVP** 단계입니다.
- ✅ **Layered Architecture**: 유지보수성을 극대화한 3계층 구조 설계.
- ✅ **PostgreSQL 연동**: Supabase를 활용한 클라우드 데이터베이스 인프라 구축.
- ✅ **게시글 CRUD**: 비동기 처리를 지원하는 게시글 관리 API 구현.
- ✅ **스키마 검증**: Pydantic을 활용한 엄격한 입출력 데이터 유효성 검사.

### **2. Future Roadmap (Planned)**
지식 플랫폼으로의 도약을 위해 다음 기능들을 순차적으로 구현할 예정입니다.
- ⬜ **Data Optimization**: Pagination 및 고도화된 검색 엔진 도입.
- ⬜ **Knowledge Ingestion**: 다양한 형식의 문서(PDF, Markdown) 업로드 기능.
- ⬜ **RAG Pipeline**: LangChain 기반의 문서 Chunking 및 Vector Embedding.
- ⬜ **AI Interaction**: 저장된 지식을 기반으로 한 맥락 기반 질의응답(RAG).
- ⬜ **Local LLM**: 보안이 중요한 조직을 위한 Ollama(로컬 모델) 연동 지원.

---

## Folder Structure
```text
backend/app/
├── api/v1/          # [구현완료] API 엔드포인트 및 라우팅
├── core/            # [구현완료] 보안 및 DB 연결 설정
├── models/          # [구현완료] SQLAlchemy 기반 데이터베이스 모델
├── schemas/         # [구현완료] Pydantic 데이터 검증 스키마
├── repositories/    # [구현완료] 데이터 접근 계층 (추상화)
├── services/        # [진행중] 비즈니스 로직 및 AI 파이프라인 확장 영역
└── main.py          # [구현완료] 앱 진입점