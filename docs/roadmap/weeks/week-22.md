# Week 22: Evaluation & Observability for LLM/Agent Systems

## Phase
Phase 7 — Evaluation & Production

## Where this fits
- **Prerequisites:** Phases 3–6 (RAG, agents, automation to observe).
- **Next:** Week 23 (deployment, security, cost/latency).

## Why this week matters
The single biggest gap between mid- and senior-level engineers is **measurement**. Agents and LLM apps are non-deterministic, so you must trace what they do, evaluate quality systematically, and catch regressions before users do. Observability and evaluation are what make agentic systems trustworthy in production.

## Learning objectives
1. Trace LLM/agent runs (inputs, tool calls, tokens, latency, cost).
2. Build evaluation datasets and automated eval/regression gates.
3. Use LangSmith and Langfuse for tracing and evaluation.

## Topics to master (in detail)
### A. Observability / tracing
- Tracing a full agent run (steps, tool calls, retries)
- **LangSmith** (hosted, free tier) and **Langfuse** (OSS, self-host)
- OpenTelemetry basics for vendor-neutral tracing
- Capturing token usage, latency, and cost per step

### B. Evaluation
- Offline eval sets and metrics (task success, faithfulness, relevance)
- LLM-as-judge: scoring outputs (and its pitfalls)
- Agent-specific eval: did it pick the right tools/path?
- promptfoo / pytest-based eval harnesses

### C. Regression gates
- Golden datasets and thresholds
- Failing CI when quality/latency/cost regresses
- Continuous evaluation on production traces

## Tools for this week
- LangSmith, Langfuse (Docker), promptfoo, pytest

## Guided coding labs
1. Instrument your agent with Langfuse or LangSmith tracing.
2. Build an eval set and score outputs with an LLM judge.
3. Add a regression gate that fails when success rate drops.

## Mini project
**Evaluation & observability harness** — tracing on your Week 21 automation plus an eval suite with a regression gate and a metrics dashboard/report. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Traced runs (screenshots/exports)
- Eval report with metrics + thresholds
- Notes: a regression you caught

## Checkpoints before moving on
- Every agent run is traceable end to end.
- You can quantify quality and block regressions automatically.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Tracing setup: 3h
3. Eval harness: 3h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
