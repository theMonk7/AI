# Master Roadmap — Agentic AI Engineering (24 Weeks)

> Goal: take you from Python developer to **mid/senior-level Agentic AI Engineer**.
> You will master: async Python for AI, LLM app fundamentals, RAG pipelines, LangChain + LangGraph, building custom agents and multi-agent systems, agent skills + MCP, agentic automation with n8n, plus evaluation, observability, and production deployment — ending in a portfolio-grade capstone.

## Who this plan is for (your starting point)
- You know Python; you are learning async Python here (Weeks 1–3).
- You know ML basics (regression) conceptually; heavy math is NOT required.
- Every concept is taught book-style: plain explanation → real-world analogy → code example → use cases → common mistakes.
- Tools chosen are in-demand in industry and mostly free / open-source.

## How the journey is ordered (and why)
1. **Solidify async + production Python** first — every AI system is I/O-bound network code.
2. **Understand LLMs and structured outputs** — the raw material of everything else.
3. **Build RAG pipelines** — the #1 real-world LLM application pattern.
4. **Learn LangChain + LangGraph** — the industry-standard orchestration layer.
5. **Build agents and multi-agent systems** — the core of "agentic AI."
6. **Automate with agentic AI (n8n)** — connect agents to real event-driven workflows.
7. **Evaluate, observe, and productionize** — what separates mid from senior.
8. **Capstone** — integrate everything into one autonomous system.

---

## Phase map

| Phase | Weeks | Theme | Outcome |
|---|---|---|---|
| 1 | 1–3 | Async & production Python for AI | Reliable, concurrent, tested Python clients |
| 2 | 4–6 | LLM application fundamentals | Prompting, structured outputs, tool calling, embeddings |
| 3 | 7–10 | RAG pipelines | Ingestion → retrieval → reranking → evaluation |
| 4 | 11–14 | LangChain & LangGraph | Chains (LCEL) + stateful graph orchestration |
| 5 | 15–18 | Agents & agentic AI | Custom agents, multi-agent, memory, skills, MCP |
| 6 | 19–21 | Agentic automation | n8n workflows driven by agents |
| 7 | 22–23 | Evaluation & production | Tracing, eval harnesses, guardrails, deployment |
| 8 | 24 | Capstone | End-to-end autonomous agentic assistant |

---

## Week-by-week index

### Phase 1 — Async & Production Python (Weeks 1–3)
- **Week 1** — Environment, reproducibility, async fundamentals, first live-API project · weeks/week-01/README.md
- **Week 2** — Concurrency deepening + failure isolation & resilience · weeks/week-02/sessions/session-01.md
- **Week 3** — Production Python toolkit: Pydantic v2 deep, typed clients, streaming, async testing · weeks/week-03.md

### Phase 2 — LLM Application Fundamentals (Weeks 4–6)
- **Week 4** — How LLMs work + calling LLM APIs (OpenAI + local Ollama) + prompt engineering · weeks/week-04.md
- **Week 5** — Structured outputs, function/tool calling, output parsing, guardrails · weeks/week-05.md
- **Week 6** — Embeddings, vector similarity, semantic search, your first (naive) RAG · weeks/week-06.md

### Phase 3 — RAG Pipelines (Weeks 7–10)
- **Week 7** — Document ingestion & chunking strategies · weeks/week-07.md
- **Week 8** — Vector stores & retrieval (FAISS, Qdrant, hybrid BM25 + dense) · weeks/week-08.md
- **Week 9** — Advanced RAG (reranking, query transforms, HyDE, multi-query, contextual retrieval) · weeks/week-09.md
- **Week 10** — RAG evaluation (RAGAS) + production RAG service · weeks/week-10.md

### Phase 4 — LangChain & LangGraph (Weeks 11–14)
- **Week 11** — LangChain core: LCEL, runnables, prompts, models, parsers · weeks/week-11.md
- **Week 12** — LangChain retrieval, memory, tools; RAG in LangChain · weeks/week-12.md
- **Week 13** — LangGraph fundamentals: state, nodes, edges, routing, cycles · weeks/week-13.md
- **Week 14** — LangGraph advanced: persistence, human-in-the-loop, streaming, subgraphs · weeks/week-14.md

### Phase 5 — Agents & Agentic AI (Weeks 15–18)
- **Week 15** — Agent fundamentals: ReAct, tool-calling loop, chains vs agents · weeks/week-15.md
- **Week 16** — Build a custom agent from scratch + LangGraph agents · weeks/week-16.md
- **Week 17** — Multi-agent systems: supervisor, hierarchical, CrewAI, AutoGen · weeks/week-17.md
- **Week 18** — Agent memory, skills, tools, and MCP (Model Context Protocol) · weeks/week-18.md

### Phase 6 — Agentic Automation (Weeks 19–21)
- **Week 19** — n8n fundamentals + integrating Python/LLM services · weeks/week-19.md
- **Week 20** — Agentic automation in n8n + orchestrator comparison (Make, Airflow, Prefect) · weeks/week-20.md
- **Week 21** — Build an agentic automation system (RAG + agent + n8n) · weeks/week-21.md

### Phase 7 — Evaluation & Production (Weeks 22–23)
- **Week 22** — Evaluation & observability (LangSmith, Langfuse, tracing, eval harnesses) · weeks/week-22.md
- **Week 23** — Production: deployment, Docker, caching, cost/latency, security & prompt-injection defense · weeks/week-23.md

### Phase 8 — Capstone (Week 24)
- **Week 24** — Capstone: end-to-end autonomous agentic assistant · weeks/week-24.md

---

## What "mid/senior-level" means by the end
- **Mid-level:** You can build a working RAG chatbot, a tool-calling agent, and an n8n automation, and wire them to an API.
- **Senior-level:** You can choose the right architecture, justify trade-offs (cost, latency, reliability), evaluate quality with metrics, add guardrails and observability, defend against prompt injection, and ship to production.

## Cadence
- 8–10 hours/week. Weekly loop: **learn → build → test → reflect.**
- Each week produces evidence (code + artifact + notes) logged in progress_tracker.md.
- Projects are given to you as a brief + skeleton with TODOs and a grading rubric; you implement, submit, and each is graded.
