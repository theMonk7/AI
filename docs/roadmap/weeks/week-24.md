# Week 24: Capstone — End-to-End Autonomous Agentic Assistant

## Phase
Phase 8 — Capstone

## Where this fits
- **Prerequisites:** All prior weeks (async, LLMs, RAG, LangChain/LangGraph, agents, automation, eval, production).
- **Next:** Portfolio packaging + interview readiness.

## Why this week matters
The capstone proves mid/senior capability by integrating the entire curriculum into one coherent, deployed, evaluated, and secured system. It becomes the centerpiece of your portfolio and the story you tell in interviews: not just "I built a chatbot," but "I designed, evaluated, and shipped an autonomous agentic system with trade-offs I can defend."

## Capstone goal
Build an **autonomous agentic assistant** that:
1. Ingests a knowledge base and answers with grounded, cited RAG (Phases 2–3).
2. Uses a multi-step agent (or multi-agent team) with tools + memory (Phases 4–5).
3. Is triggered and orchestrated through automation (Phase 6, n8n).
4. Is traced, evaluated with metrics, and guarded by a regression gate (Phase 7).
5. Is deployed via Docker Compose with caching, guardrails, and prompt-injection defenses (Phase 7).

## Suggested capstone domains (pick one)
- Personal research assistant (ingest papers/notes → research + write cited reports)
- Support/ticket triage assistant (classify → retrieve → draft → human-approve → act)
- Codebase/docs assistant (answer questions + perform safe automated actions)
- Ops assistant (monitor events → diagnose via tools/RAG → propose/execute fixes with approval)

## Required components (definition of done)
### A. Retrieval
- Ingestion + chunking + hybrid retrieval + reranking + citations

### B. Agent(s)
- Agent loop with tools, memory, and guardrails (max steps, timeouts, approvals)
- Multi-agent if the domain warrants it (supervisor + workers)
- Optionally expose tools via MCP

### C. Automation
- n8n workflow that triggers the assistant and handles human approval + errors

### D. Evaluation & observability
- Tracing (LangSmith/Langfuse), an eval set, metrics, and a regression gate

### E. Production
- Docker Compose stack, caching, rate limits, output guardrails, injection defenses
- README with architecture diagram and trade-off writeup

## Deliverables / evidence
- Running system (Compose up from a clean machine)
- Architecture diagram + decision/trade-off document
- Evaluation report with metrics and thresholds
- Demo script/recording of an end-to-end run
- Security/threat model + injection-defense demo

## Grading rubric (senior-readiness)
| Area | Weight | What "senior" looks like |
|---|---|---|
| Architecture & trade-offs | 20 | Justified choices (cost/latency/reliability) |
| RAG quality | 15 | Measured faithfulness/relevance, good citations |
| Agent design | 20 | Robust loop, tools, memory, guardrails |
| Automation | 10 | Reliable trigger→act flow with HITL |
| Evaluation & observability | 15 | Tracing + metrics + regression gate |
| Production & security | 15 | Deploys cleanly; defends against injection |
| Communication | 5 | Clear docs + trade-off narrative |

## Suggested split (multi-session; 8–10 hours minimum, extend as needed)
1. Design & scope: 1.5h
2. Integrate components: 5h+
3. Eval + hardening: 2h+
4. Docs + demo + reflection: 1.5h

## Session reflection
- What was hard:
- What is now clear:
- What I can now confidently claim on a resume / in interviews:
