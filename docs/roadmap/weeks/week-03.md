# Week 03: Production Python Toolkit for AI

## Phase
Phase 1 — Async & Production Python

## Where this fits
- **Prerequisites:** Weeks 1–2 (async fundamentals, concurrency, resilience).
- **Next:** Week 4 begins LLM application fundamentals — you'll call real LLM APIs using the typed, tested client patterns you build here.

## Why this week matters
Every AI/agent system is, underneath, a pile of async network calls returning messy JSON that must be validated. Before touching LLMs, you need a production toolkit: strong data models, typed clients, streaming, and tests. This is the difference between a demo that breaks and a service that survives real inputs.

## Learning objectives
By the end you can:
1. Model complex data with Pydantic v2 and validate untrusted input at boundaries.
2. Build a reusable typed async HTTP client with retries, timeouts, and error handling.
3. Consume streaming responses (the way LLM token streams work).
4. Write deterministic async tests with pytest + pytest-asyncio.

## Topics to master (in detail)
### A. Pydantic v2 deep
- `BaseModel`, `Field`, defaults, aliases, `model_config`
- Validation: `field_validator`, `model_validator`, constrained types
- Serialization: `model_dump`, `model_dump_json`, `model_validate`
- Nested models, `Optional`/`List` (Python 3.9 typing rules), enums
- When to use dataclasses vs Pydantic models

### B. Typed async clients
- Wrapping `httpx.AsyncClient` with a class; connection reuse
- Central retry/timeout policy (tenacity) and error taxonomy
- Parsing responses into Pydantic models (never pass raw dicts around)

### C. Streaming & backpressure basics
- Async generators (`async for`), streaming HTTP responses
- Why LLM APIs stream tokens and how to consume them

### D. Testing & logging
- `pytest-asyncio`, fixtures, mocking network with `respx`/monkeypatch
- Deterministic tests, structured logging, tracing a request end-to-end

## Tools for this week
- Pydantic v2, httpx, tenacity, pytest, pytest-asyncio, respx, python-dotenv

## Guided coding labs
1. Build a `TypedApiClient` class that fetches JSON and returns validated Pydantic models.
2. Add a streaming endpoint consumer using an async generator.
3. Write tests that mock the network and assert retry/timeout behavior.

## Mini project
**Typed, tested API client library** — a small reusable module that fetches from a public API, validates responses into models, retries transient errors, streams a large response, and has a passing test suite. (Delivered as a brief + skeleton with a grading rubric.)

## Deliverables / evidence
- `src/weeks/week_03/...` client module + models
- Passing `pytest -q` output
- Short note: "where validation caught bad data"

## Checkpoints before moving on
- All external data is validated into typed models before use.
- Tests fail on regressions and pass deterministically.
- You can explain retry + timeout interaction from memory.

## Suggested study split (8–10 hours)
1. Concept learning: 2.5h
2. Guided implementation: 4h
3. Testing and debugging: 1.5h
4. Reflection and notes: 1–2h

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
