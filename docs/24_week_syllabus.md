# 24-Week Syllabus (Beginner to Advanced)

## Phase 0: Setup and Learning OS

### Week 1
- Topic: Environment, tooling, workflow discipline
- Concepts:
  - project structure
  - API key management
  - reproducibility
- Build:
  - local dev setup
  - run starter async modules
- Deliverable:
  - setup checklist + first run logs

## Phase 1: Async Python and Reliability

### Week 2
- Topic: Async fundamentals
- Concepts:
  - event loop
  - coroutines
  - `await`, `gather`, `Semaphore`
- Build:
  - concurrent task runner
- Deliverable:
  - script comparing sequential vs concurrent runtime

### Week 3
- Topic: Resilience patterns
- Concepts:
  - timeout handling
  - retry with backoff
  - idempotency keys
- Build:
  - fault-tolerant API wrapper
- Deliverable:
  - retry logs and error report

### Week 4
- Topic: Testing and observability
- Concepts:
  - structured logs
  - unit tests for async code
  - basic service metrics
- Build:
  - tests for async and retry modules
- Deliverable:
  - test report + runtime traces

## Phase 2: LLM Core

### Week 5
- Topic: Prompt contracts and schemas
- Concepts:
  - system/user/tool roles
  - JSON schema outputs
  - failure handling
- Build:
  - strict structured output parser
- Deliverable:
  - validated response pipeline

### Week 6
- Topic: Tool calling patterns
- Concepts:
  - tool interface design
  - safe argument validation
  - model fallback patterns
- Build:
  - CLI assistant with tool stubs
- Deliverable:
  - working command loop and logs

## Phase 3: RAG (Weeks 7-10)

### Week 7
- Ingestion, chunking, metadata normalization

### Week 8
- Embeddings and vector indexes (FAISS/Qdrant)

### Week 9
- Hybrid retrieval and reranking

### Week 10
- RAG evaluation harness (faithfulness/relevance/citations)

## Phase 4: LangChain and Workflow Graphs (Weeks 11-13)

### Week 11
- LangChain primitives: models, prompts, retrievers, tools

### Week 12
- Stateful workflow design (graph thinking)

### Week 13
- Planner-executor-reviewer pipeline

## Phase 5: Automation Tools (Weeks 14-16)

### Week 14
- n8n fundamentals (nodes, triggers, webhooks)

### Week 15
- n8n + Python services integration

### Week 16
- Airflow and Prefect OSS comparison via equivalent flows

## Phase 6: Agentic Systems (Weeks 17-19)

### Week 17
- Multi-agent role design

### Week 18
- Long-horizon decomposition and memory patterns

### Week 19
- Recovery strategies and tool sandboxing

## Phase 7: Evaluation and Productionization (Weeks 20-22)

### Week 20
- Eval benchmarks and regression suites

### Week 21
- Tracing, monitoring, and cost controls

### Week 22
- Deployment blueprint (local-first to cloud)

## Phase 8: Capstone (Weeks 23-24)

### Week 23
- Build complete system and validate reliability

### Week 24
- Final demo, architecture review, and portfolio packaging
