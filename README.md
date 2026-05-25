# TraceBoard AI

> **단순한 기록을 넘어, AI가 이해하는 지식으로.**  
> TraceBoard AI는 게시판 데이터를 기반으로 **RAG(Retrieval-Augmented Generation)** 파이프라인을 구축하여  
> 저장된 정보를 활용한 AI 질의응답을 제공하는 백엔드 프로젝트입니다.

---

## 🚀 Project Overview
TraceBoard AI는 단순 CRUD 게시판을 넘어 **저장된 데이터를 “검색 가능한 지식”으로 변환하는 시스템**입니다.  
사용자가 작성한 게시글은 단순히 저장되는 것이 아니라

- → 임베딩을 통해 Vector DB에 저장되고
- → 이후 AI 질의응답의 근거 데이터로 활용됩니다.

---

## 🔥 Key Features
- 게시글 CRUD API (FastAPI + PostgreSQL)
- 게시글 기반 RAG 인덱싱
- Vector DB(Chroma) 기반 유사도 검색
- LLM(Gemini) 기반 질의응답 API
- metadata 기반 source 추적 가능

---

## 🧠 How It Works (핵심 흐름)

### 1️⃣ Indexing Flow (데이터 → 지식화)
1. 게시글 생성
2. PostgreSQL 저장
3. Embedding 생성
4. Vector DB(Chroma)에 저장
5. metadata(post_id, title, content) 함께 저장

👉 **단순 데이터 → 검색 가능한 지식으로 변환**

---

### 2️⃣ Query Flow (지식 → 답변 생성)
1. 사용자 질문 입력
2. Vector DB에서 유사 문서 검색
3. 검색 결과 → context 구성
4. LLM(Gemini)에 전달
5. 답변 + 출처(source) 반환

👉 **저장된 데이터를 기반으로 신뢰 가능한 답변 생성**

---

## 🏗️ Architecture
본 프로젝트는 **Layered Architecture** 기반으로 설계되었습니다.

```mermaid
graph LR
    A[Client] --> B[API (Router)]
    B --> C[Service (RAG)]
    C --> D[Repository]
    D --> E[Database]
    D --> F[Vector DB]
```

- **Router**: 요청/응답 처리
- **Service**: 비즈니스 로직 및 RAG 처리
- **Repository**: DB 및 Vector DB 접근

> 👉 자세한 구조는 `docs/architecture.md` 참고

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- Pydantic v2

### Database
- PostgreSQL (Supabase)

### AI / Data
- Vector DB: Chroma
- LLM: Gemini
- Pipeline: RAG (Retrieval-Augmented Generation)

---

## 📂 Folder Structure
​
```text
backend/app/
├── api/v1/          # API 엔드포인트
├── core/            # 설정 및 DB 연결
├── models/          # DB 모델
├── schemas/         # 요청/응답 스키마
├── repositories/    # 데이터 접근 계층
├── services/        # 비즈니스 로직 (RAG 포함)
└── main.py          # 앱 진입점
```

---

## 📌 API
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/ai/index-post/{post_id}` | 특정 게시글 인덱싱 (게시글 생성 시 자동 트리거) |
| `POST` | `/ai/query` | 저장된 지식 기반 AI 질의응답(RAG) 수행 |

> **Note**: `/ai/index-post` API는 게시글 생성 API 호출 시 백그라운드 태스크를 통해 자동으로 트리거되도록 설계되었습니다.
> 👉 전체 엔드포인트와 데이터 스키마는 `docs/api_spec.md` 참고.

---

## 📈 Development Status

### ✅ Current (MVP)
- **Layered Architecture**: "변하는 것과 변하지 않는 것"의 분리를 통한 유연한 설계
- **Event-driven 자동 인덱싱**: 게시글 생성 시 `FastAPI BackgroundTasks`를 활용한 비동기 인덱싱 트리거
- **Critical Path Async**: 응답 속도 최적화를 위해 핵심 파이프라인(생성/인덱싱) 우선 비동기화
- **Database**: PostgreSQL(Supabase) 및 Chroma DB(빠른 실험을 위한 로컬 벡터 저장소) 활용

### 🚧 Future
- 검색 고도화 (필터링, 정렬)
- Vector DB 확장 (Pinecone 등)
- Local LLM 연동

---

## 💡 Key Design Decisions

### 1. RAG 구조 선택
- 단순 LLM 응답이 아닌 **데이터 기반 응답**을 위해 RAG 채택

### 2. Layered Architecture
- 관심사 분리를 통해 유지보수성과 확장성 확보

### 3. Vector DB 분리
- PostgreSQL: 원본 데이터 저장
- Vector DB: 의미 기반 검색

---

## 🧪 Technical Notes & Trade-offs

### 1. 비동기 처리와 BackgroundTasks
- **Latency 최적화**: 무거운 Embedding 작업을 백그라운드로 분리하여 사용자 응답 속도를 극대화했습니다.
- **의존성 분리**: Background Task 내에서는 요청 스코프(Request Scope)의 DB 세션을 공유할 수 없으므로, **별도의 세션을 생성하여 작업을 수행**하도록 설계하여 안정성을 확보했습니다.
- **한계 및 확장**: 현재 방식은 서버 재시작 시 작업 유실 가능성이 있으며, 이를 보완하기 위해 향후 **Redis 기반의 Message Queue(Celery)** 도입을 고려하고 있습니다.

### 2. Vector DB 선택 이유
- MVP 단계에서 별도의 인프라 구축 비용 없이 빠른 실험과 로컬 환경 구성을 위해 **Chroma**를 선택했습니다. 데이터 규모 확장에 따라 Pinecone 등 클라우드 기반 Vector DB로의 전환을 염두에 두고 있습니다.