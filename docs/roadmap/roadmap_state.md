# Roadmap State (Single Source of Truth)

- Current date baseline: 2026-06-10
- Program duration: 24 weeks
- Weekly commitment: 8 to 10 hours
- Current active week: Week 2
- Current status: In progress
- Next immediate action: Grade Week 2 project when submitted, then start Week 3 (production Python toolkit)

## Roadmap revision note (2026-07-09)
- Curriculum was comprehensively re-planned to target mid/senior Agentic AI Engineer.
- New phase structure (see master_roadmap.md):
  - Phase 1 (W1-3): Async & production Python
  - Phase 2 (W4-6): LLM app fundamentals (LLM internals, prompting, structured outputs/tool calling, embeddings)
  - Phase 3 (W7-10): RAG pipelines (ingestion, retrieval/hybrid, advanced RAG, evaluation)
  - Phase 4 (W11-14): LangChain (LCEL) + LangGraph (state graphs, persistence, HITL)
  - Phase 5 (W15-18): Agents & agentic AI (ReAct, custom agent from scratch, multi-agent, memory/skills/MCP)
  - Phase 6 (W19-21): Agentic automation with n8n (+ Prefect/Airflow/Make comparison)
  - Phase 7 (W22-23): Evaluation/observability (LangSmith/Langfuse) + production/security
  - Phase 8 (W24): Capstone — end-to-end autonomous agentic assistant
- Weeks 3-24 detailed content written; week-01/02 preserved (already taught).

## Completed weeks
- Week 1 (completed 2026-07-08): Environment setup, async fundamentals, concurrency patterns, reliability, Pydantic, FastAPI, mini-project

## In-progress week notes
- Week 2 (Phase 1): async concurrency at production depth.
- Focus: event loop internals, gather vs create_task, bounded concurrency, failure isolation.
- Session 1 done: concurrency deepening (docs .../week-02/sessions/session-01.md + src .../week_02/foundations/session1_concurrency_deepening.py).
- Session 2 done: failure isolation & resilient concurrency (docs .../week-02/sessions/session-02.md + src .../week_02/foundations/session2_resilient_concurrency.py). Verified exit 0.
- Session 3 done: async pipelines — queues, worker pools, backpressure, graceful shutdown, rate limiting (docs .../week-02/sessions/session-03.md + src .../week_02/foundations/session3_async_pipeline.py). Verified exit 0.
- Week 2 END-OF-WEEK PROJECT issued (cumulative W1-2): Concurrent Web Fetch Pipeline — brief+skeleton at src/weeks/week_02/projects/week02_async_scraper_pipeline.py (25-pt rubric). Awaiting user submission to grade.
- Week 2 README added: docs/roadmap/weeks/week-02/README.md.

## Week 1 closure evidence
- Session 1 code: src/weeks/week_01/foundations/module1_session1_async.py
- Session 2 code: src/weeks/week_01/foundations/async_patterns.py, reliable_client.py
- Session 3 code: src/weeks/week_01/llm_core/structured_outputs.py, agent_echo_api.py
- Mini-project: src/weeks/week_01/projects/week01_live_api_status.py
- Artifact: artifacts/week01/api_health_report.json
- Assignment completed: MonitorReport model, /agent/status endpoint, multiple-of-15 validator

## Blockers
- None

## How to update after each session
1. Update current status and active week.
2. Append evidence links to progress_tracker.md.
3. Add short reflection under the current week file.
