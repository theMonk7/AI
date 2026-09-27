# Week 21: Build an Agentic Automation System (RAG + Agent + n8n)

## Phase
Phase 6 — Agentic Automation

## Where this fits
- **Prerequisites:** Weeks 19–20 (n8n, agentic workflows).
- **Next:** Phase 7 (evaluation & production) — make it trustworthy and shippable.

## Why this week matters
This is the Phase 6 capstone: you integrate everything so far — a RAG service, an agent, and n8n orchestration — into one **event-driven agentic automation** that does real work end to end. This mirrors exactly the kind of system in-demand at companies adopting agentic AI.

## Learning objectives
1. Architect an end-to-end agentic automation (trigger → agent → tools/RAG → action).
2. Add human-in-the-loop approval and error recovery.
3. Log every run for later evaluation (Phase 7).

## Topics to master (in detail)
### A. System design
- Choosing triggers (webhook, schedule, email/chat)
- Where the agent lives (in n8n vs your service) and why
- Wiring RAG + tools as agent capabilities
- State/memory across workflow runs

### B. Reliability & safety
- Approval gates before consequential actions
- Retries, timeouts, dead-letter paths, cost caps
- Idempotency for repeated triggers

### C. Observability hooks
- Structured logs/traces for each step (feeds Week 22)
- Capturing inputs/outputs for evaluation

## Tools for this week
- n8n, your RAG + agent services, a datastore (Postgres/Redis), Docker

## Guided coding labs
1. Design the architecture diagram + data flow for your automation.
2. Implement the trigger → agent → RAG/tools → action pipeline.
3. Add a HITL approval step and error-recovery path.

## Mini project (Phase 6 capstone)
**End-to-end agentic automation** — e.g., an inbox/ticket assistant: trigger on new item → agent researches via RAG/tools → drafts action → human approves → executes, with full logging. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Running end-to-end automation (workflow + services)
- Architecture diagram + run logs
- Notes: failure modes and how you handled them

## Checkpoints before moving on
- A real trigger drives an agent that uses RAG/tools to complete a task.
- Consequential actions require approval.
- Every run is logged for evaluation.

## Suggested study split (8–10 hours)
1. Design: 1.5h
2. Build: 5h
3. Hardening: 1.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
