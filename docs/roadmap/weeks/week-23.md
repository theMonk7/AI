# Week 23: Production — Deployment, Cost/Latency, Security & Guardrails

## Phase
Phase 7 — Evaluation & Production

## Where this fits
- **Prerequisites:** Week 22 (eval & observability).
- **Next:** Week 24 (capstone integrating everything).

## Why this week matters
Shipping an agentic system to production is where senior engineering shows: containerized deployment, caching and cost/latency control, and — critically — **security against prompt injection and unsafe tool use**. Agents that take actions are a real attack surface; defending them is a defining senior skill.

## Learning objectives
1. Containerize and deploy your services with Docker/Compose.
2. Control cost and latency (caching, model routing, streaming).
3. Defend against prompt injection and unsafe tool execution.

## Topics to master (in detail)
### A. Deployment
- Dockerize FastAPI services; Docker Compose for the full stack (app, vector DB, Redis)
- Config/secrets management; environment separation
- Health checks, graceful shutdown, and horizontal scaling basics

### B. Cost & latency engineering
- Caching (prompt/response, embeddings) with Redis
- Model routing (small model for easy tasks, large for hard)
- Streaming, batching, and token-budget discipline
- Rate limiting and backpressure

### C. Security & guardrails (critical)
- **Prompt injection**: what it is, direct vs indirect (via retrieved/tool data)
- Defenses: input/output filtering, allow-lists, sandboxing tools, least privilege
- Never trusting tool arguments; approval gates for side effects
- PII handling, secrets, and data governance basics
- Guardrails-AI / NeMo Guardrails for output validation

## Tools for this week
- Docker + Compose, Redis, LiteLLM (routing), Guardrails-AI/NeMo Guardrails

## Guided coding labs
1. Dockerize your stack (app + vector DB + Redis) with Compose.
2. Add response/embedding caching and measure latency/cost savings.
3. Demonstrate a prompt-injection attack, then defend against it.

## Mini project
**Production-hardened service** — your agent/RAG deployed via Compose with caching, rate limits, output guardrails, and prompt-injection defenses, plus a short threat model. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Compose stack that runs from a clean machine
- Cost/latency before-after numbers
- Threat model + injection defense demo

## Checkpoints before moving on
- The system runs reproducibly via Docker Compose.
- You can show measurable cost/latency improvements.
- You can demonstrate and defend against a prompt-injection attack.

## Suggested study split (8–10 hours)
1. Deployment: 3h
2. Cost/latency: 2h
3. Security & guardrails: 3h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
