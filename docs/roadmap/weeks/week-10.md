# Week 10: RAG Evaluation & a Production RAG Service

## Phase
Phase 3 — RAG Pipelines

## Where this fits
- **Prerequisites:** Weeks 7–9 (ingestion, retrieval, advanced RAG).
- **Next:** Phase 4 (LangChain/LangGraph) — you'll rebuild and orchestrate RAG with industry frameworks.

## Why this week matters
"It looks good when I try it" is not evidence. Senior engineers *measure* RAG quality with metrics and catch regressions automatically. This week you learn to evaluate faithfulness, relevance, and grounding, then wrap your pipeline as a real service. This is the Phase 3 capstone.

## Learning objectives
1. Evaluate RAG with metrics (faithfulness, answer relevance, context precision/recall).
2. Build an evaluation set and a repeatable eval harness.
3. Serve RAG behind a FastAPI endpoint with citations, cost, and latency tracking.

## Topics to master (in detail)
### A. Why & what to evaluate
- Hallucination, groundedness, relevance — defined
- Retrieval metrics (context precision/recall) vs generation metrics (faithfulness, answer relevance)
- Building a gold Q&A eval set from your corpus

### B. Evaluation tooling
- **RAGAS** metrics and how to run them
- LLM-as-judge (benefits and pitfalls)
- Regression testing: fail the build when quality drops

### C. Production RAG service
- FastAPI endpoint: question in → grounded answer + citations out
- Latency & cost tracking per request
- Caching, and graceful "I don't know" when retrieval is weak

## Tools for this week
- RAGAS, pytest, pandas, FastAPI, your Week 9 pipeline

## Guided coding labs
1. Build a 20-question eval set and score your pipeline with RAGAS.
2. Add a regression test that fails if faithfulness drops below a threshold.
3. Wrap the pipeline in a FastAPI endpoint with citations + metrics.

## Mini project (Phase 3 capstone)
**Production RAG service** with an evaluation harness: measurable faithfulness/relevance, regression gate, and a served API returning grounded, cited answers. (Brief + skeleton + rubric.)

## Deliverables / evidence
- Eval report (metrics table) artifact
- RAG API returning citations + latency/cost
- Notes: your quality thresholds and why

## Checkpoints before moving on
- You can quantify your RAG's quality with metrics.
- A regression gate protects against quality drops.
- The service returns grounded, cited answers.

## Suggested study split (8–10 hours)
1. Concept learning: 2h
2. Eval harness build: 3.5h
3. Service + tracking: 2.5h
4. Reflection and notes: 1h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
