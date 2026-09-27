# Tool Catalog (In-Demand + Mostly Open-Source)

Tools are chosen for two reasons: **industry demand** and **free/OSS or generous free tier**. First-introduced week is noted so you learn each tool in context.

## Core coding stack (Weeks 1–3)
- Python 3.9+ (this repo uses 3.9 — mind the typing rules)
- FastAPI — API layer for serving agents/RAG
- Pydantic v2 — data validation & structured outputs
- pytest + pytest-asyncio — testing async code
- httpx + tenacity — async HTTP + retries
- python-dotenv — config/secrets hygiene

## LLM access & prompting (Weeks 4–6)
- OpenAI API (hosted, industry default)
- **Ollama** — run open models locally, free (Llama, Mistral, Qwen, etc.)
- LiteLLM — one interface across many providers
- tiktoken — token counting/cost estimation
- instructor / Pydantic-AI — structured outputs from LLMs

## RAG stack (Weeks 6–10)
- sentence-transformers — local embeddings (free)
- FAISS — fast local vector index
- **Qdrant** (OSS) — production vector database
- Chroma — lightweight local vector store
- rank-bm25 — keyword/sparse retrieval for hybrid search
- cross-encoder rerankers (sentence-transformers) / Cohere Rerank (API)
- unstructured / pypdf / markdown loaders — document ingestion
- **RAGAS** — RAG evaluation metrics

## Orchestration: LangChain & LangGraph (Weeks 11–14)
- LangChain (LCEL, runnables, retrievers, tools)
- **LangGraph** — stateful, cyclic agent/workflow graphs
- LangChain community integrations

## Agent frameworks (Weeks 15–18)
- LangGraph agents (primary)
- **CrewAI** — role-based multi-agent (OSS)
- **AutoGen** (Microsoft) — conversational multi-agent (OSS)
- OpenAI Agents SDK (optional, hosted)
- **MCP (Model Context Protocol)** — standard for connecting tools/data to agents

## Automation stack (Weeks 19–21)
- **n8n** (primary, OSS) — event-driven workflow automation with AI nodes
- Make.com (comparison, freemium)
- Airflow (OSS) — scheduled data/ML pipelines
- Prefect (OSS) — Pythonic orchestration
- Node-RED (comparison, OSS)

## Data & infra
- PostgreSQL + pgvector — relational store + vectors
- Redis — caching, queues, short-term memory
- Docker + Docker Compose — reproducible deployment

## Evaluation & observability (Weeks 22–23)
- **LangSmith** — tracing & eval (free tier) for LangChain/LangGraph
- **Langfuse** (OSS) — self-hostable tracing & eval
- OpenTelemetry — vendor-neutral tracing
- promptfoo — prompt/regression testing
- custom eval harnesses (pytest-based)

## Security & guardrails (Week 23)
- Guardrails-AI / NeMo Guardrails — output validation & safety
- prompt-injection defenses (allow-lists, sandboxing, output filtering)
