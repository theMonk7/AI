# Week 20: Agentic Automation in n8n + Orchestrator Comparison

## Phase
Phase 6 — Agentic Automation

## Where this fits
- **Prerequisites:** Week 19 (n8n basics + integration).
- **Next:** Week 21 (build a full agentic automation system).

## Why this week matters
This is where "agentic AI" meets "automation." n8n now has native AI Agent and LLM nodes, letting workflows *reason and act*, not just move data. You'll also learn where n8n fits versus data/ML orchestrators (Airflow, Prefect) and no-code tools (Make) — the senior skill of picking the right tool for each job.

## Learning objectives
1. Build agentic workflows using n8n's AI Agent / LLM nodes.
2. Combine deterministic automation with agent decision-making.
3. Compare n8n, Make, Airflow, and Prefect and choose appropriately.

## Topics to master (in detail)
### A. Agentic n8n
- AI Agent node, LLM/chat model nodes, tool nodes, memory
- Connecting your own tools/RAG as agent tools inside n8n
- When to let the agent decide vs hardcode the path (reliability)
- Human-in-the-loop approvals inside automations

### B. Orchestrator landscape (senior judgment)
- n8n: event-driven app/AI automation (integration-heavy)
- Make.com: no-code SaaS automation (comparison)
- Airflow: scheduled DAGs for data/ML pipelines
- Prefect: Pythonic flows with dynamic control
- Choosing by trigger type, code-vs-visual, scale, and team

### C. Reliability
- Idempotency, retries, dead-letter handling, cost caps in agentic flows

## Tools for this week
- n8n (AI nodes), Prefect (OSS), Airflow (overview), Make (overview)

## Guided coding labs
1. Build an n8n AI-agent workflow that uses a tool + memory.
2. Recreate a simple scheduled pipeline in Prefect; contrast with n8n.
3. Write a decision guide: which orchestrator for which scenario.

## Mini project
**Agentic triage automation** — an n8n AI-agent workflow that classifies incoming requests, calls the right tool/RAG, and escalates to a human when unsure. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Agentic n8n workflow export
- Prefect flow + comparison writeup
- Orchestrator decision guide

## Checkpoints before moving on
- You can build an agentic (reasoning) workflow in n8n.
- You can justify n8n vs Prefect/Airflow/Make for a scenario.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Agentic n8n build: 4h
3. Prefect + comparison: 2h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
