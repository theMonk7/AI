# Week 02: Production Async — Concurrency, Resilience & Pipelines

## Phase
Phase 1 — Async & Production Python

## Week objective
Go from "async works" to "I can design safe, resilient, controlled concurrent systems and explain every trade-off." Ends with a cumulative project that applies Weeks 1–2.

## Session index
1. **Session 01** — Async Concurrency Deepening
   - Path: `docs/roadmap/weeks/week-02/sessions/session-01.md`
   - Code: `src/weeks/week_02/foundations/session1_concurrency_deepening.py`
   - Covers: concurrency internals, gather vs create_task, bounded concurrency, throughput tuning

2. **Session 02** — Failure Isolation & Resilient Concurrency
   - Path: `docs/roadmap/weeks/week-02/sessions/session-02.md`
   - Code: `src/weeks/week_02/foundations/session2_resilient_concurrency.py`
   - Covers: gather(return_exceptions), as_completed, per-task timeouts, cancellation, the robust runner (semaphore+retry+timeout+isolation)

3. **Session 03** — Async Pipelines: Queues, Worker Pools & Rate Limiting
   - Path: `docs/roadmap/weeks/week-02/sessions/session-03.md`
   - Code: `src/weeks/week_02/foundations/session3_async_pipeline.py`
   - Covers: asyncio.Queue, producer–consumer, worker pools, backpressure, graceful shutdown, rate limiting

## End-of-week project (cumulative: Weeks 1–2)
**Concurrent Web Fetch Pipeline** — a real async tool combining a worker pool, queue,
rate limiting, per-attempt timeouts, retries, failure isolation, and a validated JSON report.
- Brief + skeleton: `src/weeks/week_02/projects/week02_async_scraper_pipeline.py`
- You implement the TODOs, run it, and submit for grading (25-pt rubric in the file).

## How to run the labs
```bash
source .venv/bin/activate
python src/weeks/week_02/foundations/session1_concurrency_deepening.py
python src/weeks/week_02/foundations/session2_resilient_concurrency.py
python src/weeks/week_02/foundations/session3_async_pipeline.py
```

## Checkpoints before moving to Week 3
- You can explain: concurrency vs rate limiting, backpressure, graceful shutdown.
- You can build a queue + worker pool pipeline from memory.
- The Week 2 project runs, isolates failures, paces requests, and writes a valid artifact.

## Deliverables / evidence
- Three lab runs (terminal output)
- Completed Week 2 project + `artifacts/week02/fetch_report.json`
- Quiz answers + revision notes per session
