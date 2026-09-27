# Phase Overview and Competency Targets

Each phase builds directly on the previous one. Competencies are what you should be able to *do* (not just recognize) before advancing.

## Phase 1 — Async & Production Python (Weeks 1–3)
- Write correct async code: coroutines, `await`, event loop, `gather`, `create_task`.
- Apply bounded concurrency (Semaphore), timeouts, retries, and failure isolation.
- Model and validate data with Pydantic v2; write typed async API clients; test async code with pytest.

## Phase 2 — LLM Application Fundamentals (Weeks 4–6)
- Explain how LLMs work at a working level: tokens, context window, temperature, embeddings.
- Call LLM APIs (hosted + local via Ollama), engineer prompts, and manage cost/latency.
- Get reliable structured outputs and tool calls; understand and use embeddings for semantic search.

## Phase 3 — RAG Pipelines (Weeks 7–10)
- Ingest and chunk documents with good metadata; choose chunking strategies deliberately.
- Build retrieval over vector stores (FAISS, Qdrant) and hybrid (BM25 + dense) search.
- Apply advanced RAG (reranking, query transforms) and evaluate quality with metrics (RAGAS).

## Phase 4 — LangChain & LangGraph (Weeks 11–14)
- Compose chains with LCEL/runnables; wire retrieval, memory, tools, and output parsers.
- Build stateful graph workflows in LangGraph with routing, cycles, persistence, and human-in-the-loop.

## Phase 5 — Agents & Agentic AI (Weeks 15–18)
- Explain and implement the agent loop (ReAct, tool-calling); know when to use agents vs chains.
- Build a custom agent from scratch and with LangGraph; design multi-agent systems (supervisor/hierarchical).
- Add memory, reusable skills, and connect tools via MCP (Model Context Protocol).

## Phase 6 — Agentic Automation (Weeks 19–21)
- Build event-driven automations in n8n (triggers, nodes, webhooks) and integrate LLM/agent services.
- Design agentic automations and compare orchestrators (n8n, Make, Airflow, Prefect).

## Phase 7 — Evaluation & Production (Weeks 22–23)
- Trace, evaluate, and regression-test LLM/agent systems (LangSmith, Langfuse, eval harnesses).
- Deploy with Docker; add caching, guardrails, cost/latency control, and prompt-injection defenses.

## Phase 8 — Capstone (Week 24)
- Integrate RAG + multi-agent orchestration + automation + evaluation + deployment into one system.
- Communicate senior-level architecture and trade-off decisions.
