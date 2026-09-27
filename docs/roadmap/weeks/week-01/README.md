# Week 01: Environment Setup, Reproducibility, and First Live API Project

## Phase
Phase 0

## Week 1 folder structure
- `docs/roadmap/weeks/week-01/README.md` (this file): week overview, topics, outcomes
- `docs/roadmap/weeks/week-01/sessions/session-01.md`: async fundamentals lesson

## Topics in this week
1. Environment setup and isolation (`venv`)
2. Dependency pinning and reproducibility
3. Environment variables and config hygiene
4. Async basics and real API calls
5. Evidence-driven learning with artifacts and tests

## Session index
1. **Session 01**: Async Python Fundamentals — real API calls
   - Path: `docs/roadmap/weeks/week-01/sessions/session-01.md`
   - Code: `src/weeks/week_01/foundations/module1_session1_async.py`
   - Covers: coroutine, await, serial, parallel, dependency, cancellation, done callbacks, semaphores

2. **Session 02**: Concurrency Patterns and Reliability
   - Path: `docs/roadmap/weeks/week-01/sessions/session-02.md`
   - Code: `src/weeks/week_01/foundations/async_patterns.py`, `reliable_client.py`
   - Covers: semaphore + gather benchmark, transient vs permanent errors, retry, backoff, timeout

3. **Session 03**: Structured Outputs, FastAPI, and Mini-Project
   - Path: `docs/roadmap/weeks/week-01/sessions/session-03.md`
   - Code: `src/weeks/week_01/llm_core/structured_outputs.py`, `agent_echo_api.py`, `projects/week01_live_api_status.py`
   - Covers: Pydantic BaseModel, Field, ValidationError, nested models, field_validator, FastAPI routes, HTTPException, cumulative mini-project

## Week objective
Build a fully reproducible development environment and run your first real mini-project that hits public APIs and generates an artifact report.

## Setup (single source)
Use one setup guide only:
- `docs/setup/environment_setup.md`

## Why this week matters
Before advanced agent workflows, you need reliable local execution. Most AI engineering failures in real teams are setup, dependency, or environment drift issues, not model logic issues.

## Concepts explained (with practical meaning)
1. Isolated environment (`venv`)
- Why: prevents package/version conflicts across projects.
- Practical rule: always activate `.venv` before running code.

2. Dependency pinning (`requirements.txt`)
- Why: teammates and future-you should get the same behavior.
- Practical rule: install from repo requirements, do not mix global packages.

3. Environment variables (`.env`)
- Why: secrets/config should not be hardcoded in source files.
- Practical rule: keep `.env.example` in git, keep real `.env` local only.

4. Reproducibility
- Why: any workflow should run from a clean machine with predictable outputs.
- Practical rule: validate with a standard run sequence and a test command.

5. Execution evidence
- Why: learning should produce proof, not only understanding.
- Practical rule: generate artifacts/logs each week (`artifacts/weekXX`).

## Tools for this week
- Python 3.11+
- pip + venv
- pytest
- httpx (for live API calls)
- python-dotenv

## Hands-on labs
1. Lab A: Environment and baseline validation
- Follow `docs/setup/environment_setup.md` end-to-end.
- Run baseline scripts:
- `python src/weeks/week_01/foundations/async_patterns.py`
- `python src/weeks/week_01/foundations/reliable_client.py`
- `python src/weeks/week_01/llm_core/structured_outputs.py`
- `python -m pytest -q`

2. Lab B: Live API mini-project
- Run:
- `python src/weeks/week_01/projects/week01_live_api_status.py`
- What you should observe:
	- each endpoint status and latency
	- report JSON written to `artifacts/week01/api_health_report.json`

## Weekly mini-project (cumulative pattern starts here)
Project: Live API Status Monitor
- Inputs: a list of public endpoint URLs
- Processing: concurrent HTTP calls, status classification, latency measurement
- Output: machine-readable JSON report artifact

How this supports future weeks:
- Week 2: improve concurrency model and throughput
- Week 3: add retries/backoff and transient error policy
- Week 4: add tests and richer logging around this project

## Deliverables
- Environment setup completed via `docs/setup/environment_setup.md`
- Baseline scripts executed successfully
- `pytest` passing
- Week 1 artifact: `artifacts/week01/api_health_report.json`

## Checkpoints before moving on
- You can recreate setup from scratch in under 20 minutes.
- You can explain each setup component (venv, requirements, .env).
- Live API mini-project runs and creates the JSON artifact.

## Revision summary: all terms and definitions

---

### `async def` — Coroutine definition
**What it is:** Declares a coroutine function. Calling it does not execute the body — it returns a coroutine object.  
**Example:**
```python
async def fetch():
    await asyncio.sleep(1)
    return "done"
```
**Usage:** Any function that does I/O (network, file, DB) should be `async def` so it can yield control while waiting.

---

### `await` — Pause and resume
**What it is:** Suspends the current coroutine until the awaited task completes. While it waits, the event loop runs other pending coroutines.  
**Example:**
```python
result = await fetch()   # pauses here; event loop can run other tasks
```
**Usage:** Put `await` before every coroutine call or async I/O operation. Forgetting it means the coroutine is never actually executed.

---

### Event loop — The scheduler
**What it is:** The runtime that manages and switches between coroutines. It runs one coroutine at a time but switches to another when the current one awaits I/O.  
**Example:**
```python
asyncio.run(main())   # creates event loop, runs main, shuts down
```
**Usage:** Always use `asyncio.run()` once at the top level. Never call `asyncio.run()` inside an already-running loop.

---

### Serial execution — One at a time
**What it is:** Each coroutine starts only after the previous one finishes. Safe and predictable, but slow when tasks involve waiting.  
**Example:**
```python
for url in urls:
    result = await fetch(url)   # next starts only after this completes
```
**Usage:** Use when tasks depend on each other's output, or when ordering must be guaranteed.

---

### Parallel execution with `gather` — All at once
**What it is:** Starts multiple coroutines concurrently and waits for all of them to finish. Total time is the duration of the slowest task, not the sum.  
**Example:**
```python
results = await asyncio.gather(fetch(url1), fetch(url2), fetch(url3))
```
**Usage:** Use when tasks are independent. This is the default pattern for hitting multiple APIs.

---

### `create_task` — Scheduled task object
**What it is:** Schedules a coroutine on the event loop immediately and returns a `Task` object you can inspect, await, or cancel individually.  
**Example:**
```python
task = asyncio.create_task(fetch(url))
task.add_done_callback(on_done)
result = await task
```
**Usage:** Use instead of `gather` when you need lifecycle control — attaching callbacks, cancelling individual tasks, or tracking completion order.

---

### Done callback — On-completion hook
**What it is:** A function registered on a `Task` that fires automatically as soon as the task finishes, regardless of what order tasks complete.  
**Example:**
```python
def on_done(task):
    print("Finished:", task.result().url)

task = asyncio.create_task(fetch(url))
task.add_done_callback(on_done)
```
**Usage:** Useful for logging completion order, triggering downstream actions, or feeding a result queue as tasks finish.

---

### `Semaphore` — Concurrency limiter
**What it is:** A counter-based lock that allows at most `n` coroutines to run in a critical section at the same time.  
**Example:**
```python
sem = asyncio.Semaphore(3)

async def limited(url):
    async with sem:          # blocks here if 3 tasks already running
        return await fetch(url)
```
**Usage:** Always use a semaphore when calling external APIs in bulk. Prevents hitting rate limits, overloading downstream services, and exhausting file descriptors.

---

### Dependency chain — Sequential with data flow
**What it is:** The output of one async call is used as the input to the next. Each step `awaits` the prior result before proceeding.  
**Example:**
```python
post = await fetch_post(post_id)           # step 1
user = await fetch_user(post["userId"])    # step 2 uses step 1 data
```
**Usage:** Use for multi-step workflows where later steps need data from earlier ones, such as: look up entity → enrich with related data → store result.

---

### Cancellation — Stopping a running task
**What it is:** Requesting a `Task` to stop. It raises `CancelledError` inside the coroutine at the next `await` point. Must be caught explicitly.  
**Example:**
```python
task = asyncio.create_task(slow_fetch(url))
await asyncio.sleep(1.0)   # wait 1 second
task.cancel()              # signal cancel

try:
    await task
except asyncio.CancelledError:
    print("Task was cancelled")
```
**Usage:** Use for timeout enforcement, graceful shutdown, or abandoning slow tasks when a faster result is already available.

---

### `asyncio.sleep` vs `time.sleep` — Critical distinction
**What it is:** `asyncio.sleep` yields control back to the event loop. `time.sleep` blocks the entire thread — no other coroutine runs during that time.  
**Example:**
```python
await asyncio.sleep(1)   # correct: event loop still runs
time.sleep(1)            # wrong: blocks everything
```
**Usage:** Always use `await asyncio.sleep` inside async functions. Never use `time.sleep` in async code.

---

### `httpx.AsyncClient` — Async HTTP client
**What it is:** An async-capable HTTP client that integrates with `asyncio`. Each request is an awaitable that yields while waiting for network I/O.  
**Example:**
```python
async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
    response = await client.get("https://api.github.com")
```
**Usage:** Use this (not `requests`) for all HTTP calls inside async code. Always set an explicit `timeout` to prevent hanging.

---

## Suggested study split (8 to 10 hours)
1. Setup and environment validation: 2 hours
2. Concept deep understanding: 2 hours
3. Hands-on labs and mini-project: 3 to 4 hours
4. Debugging and reflection notes: 1 to 2 hours

## Session reflection
- What was hard:
- What is now clear:
- What to revise next week:
