# Week 2 | Session 1: Async Concurrency Deepening

## Session goal
Move from "I can run async code" to "I can design concurrent systems safely and explain every trade-off."

## Where we are in roadmap
- Phase 0 (Week 1): completed — environment, async basics, reliability, Pydantic, FastAPI, capstone project
- Phase 1 begins here (Weeks 2–4): production-grade async and resilience patterns
- This session: execution model internals, gather vs create_task, bounded concurrency, throughput tuning

## Prerequisites
- Week 1 capstone project runs cleanly
- Environment active: `source .venv/bin/activate`

---

## How to use this document
Read each chapter top to bottom. Every concept has:
1. Plain-language explanation (what it is and why it matters)
2. Real-world analogy (to build intuition)
3. Code example (to see exact syntax)
4. Use cases (when you actually reach for this tool)
5. Common mistakes (what goes wrong and why)

Run the lab file while reading. Observe numbers, then come back and re-read the theory.

---

## Theory Chapter 1: What concurrency actually gives you
Concurrency does not make each task faster. It improves total elapsed time when tasks spend significant time waiting (network, disk, DB).

If each task has:
- compute time: `C`
- wait time: `W`

## Theory Chapter 1: What concurrency actually gives you

### 1.1 The core idea in plain language
Concurrency does not make a single task run faster. It lets your program make progress on other work while one task is *waiting*. The CPU is not doing more per second; it just stops sitting idle during waits.

### 1.2 Real-world analogy: the coffee shop barista
Imagine one barista taking five orders:
- **Sequential (blocking):** They take order 1, start the espresso machine, and *stand still staring at it* for 40 seconds until it finishes. Then they start order 2. Five customers take a very long time.
- **Concurrent (async):** They take order 1, press start, and *while the machine runs* they take order 2, press start, take order 3, and so on. The machines run in parallel; the barista just coordinates. All five drinks finish far sooner.

The barista is your single CPU thread. The espresso machine's run time is the "I/O wait" (a network call, a database query, a disk read). Async lets the one worker stay busy coordinating instead of freezing on each wait.

### 1.3 The timing math (why it works)
If each task has:
- compute time `C` (CPU work the barista must actively do)
- wait time `W` (the machine running by itself)

Then for `N` tasks:

$$\text{Sequential} \approx N \times (C + W)$$
$$\text{Concurrent (ideal)} \approx (N \times C) + \max(W)$$

Interpretation:
- CPU work `C` still scales with N — the barista can only press one button at a time.
- Waiting `W` overlaps — the machines all run at once, so you pay for the *longest* wait only.

Concrete example: 10 HTTP calls, each 5ms of CPU parsing + 200ms network wait.
- Sequential: `10 × (5 + 200) = 2050ms`
- Concurrent: `(10 × 5) + 200 = 250ms`

That is an 8x improvement, and it came entirely from overlapping the waits.

### 1.4 When concurrency helps a LOT
1. **High I/O wait** — HTTP APIs, database queries, file reads, LLM calls. This is the sweet spot.
2. **Independent tasks** — no task needs another's result.
3. **A sane concurrency cap** — enough parallelism to overlap waits without overwhelming anything.

### 1.5 When concurrency barely helps (or hurts)
1. **CPU-bound work** — hashing, image processing, big math loops. There is no wait to overlap; the barista is the bottleneck. (For this, you need multiprocessing, not async.)
2. **Strict dependency chains** — if task 2 needs task 1's output, they cannot overlap.
3. **Hard external rate limits** — if the API allows 2 requests/sec, more concurrency just produces errors.

### 1.6 Common mistake
Believing async makes CPU-bound code faster. It does not. If your bottleneck is computation (not waiting), async adds overhead with no benefit. Diagnosis question to always ask: *"Is my program slow because it is waiting, or because it is computing?"*

---

## Theory Chapter 2: The event loop scheduling model

### 2.1 What the event loop is
The event loop is a single-threaded scheduler. It runs one coroutine at a time and switches to another *only* at `await` points. Nothing is truly running in parallel on the CPU — the loop is rapidly juggling many paused-and-resumed coroutines.

### 2.2 Real-world analogy: a chess master playing 20 boards
A grandmaster plays 20 opponents at once by walking down a row of boards. At each board they make one move (fast work), then move to the next board while the opponent thinks (the wait). They never stand still waiting for one opponent. One brain, 20 games "in progress."

The grandmaster is the event loop. Each board is a coroutine. Their move is the code between two `await`s. The opponent thinking is the awaited I/O.

### 2.3 Step-by-step: what happens at an await
```python
import asyncio

async def worker(name: str):
    print(f"{name}: start")
    await asyncio.sleep(1)      # <-- yield point: worker pauses here
    print(f"{name}: done")

async def main():
    await asyncio.gather(worker("A"), worker("B"))

asyncio.run(main())
```
Execution timeline:
1. `A` prints "start", hits `await asyncio.sleep(1)`, and **yields control**.
2. The loop is now free, so it starts `B`. `B` prints "start", hits its `await`, and yields.
3. Both are now paused. The loop waits ~1 second.
4. Both timers fire; the loop resumes `A` then `B`; both print "done".

Total time ≈ 1 second, not 2. The two 1-second waits overlapped.

### 2.4 The single most important rule: never block the loop
Because there is only one thread, if any coroutine refuses to yield, *everything* freezes. This is the number one async bug.

```python
import time
import asyncio

async def bad():
    time.sleep(3)          # WRONG: blocks the entire event loop for 3s
    return "done"

async def good():
    await asyncio.sleep(3) # RIGHT: yields, other coroutines keep running
    return "done"
```
With `time.sleep(3)`, the chess master sits frozen at one board for 3 seconds while 19 opponents wait. With `await asyncio.sleep(3)`, they keep circling the room.

### 2.5 What counts as "blocking"
Anything that does not yield control back to the loop:
- `time.sleep()`
- `requests.get()` (synchronous HTTP — use `httpx.AsyncClient` instead)
- Heavy CPU loops (large computations)
- Synchronous file reads on huge files
- Standard library DB drivers that are not async

### 2.6 Use cases for understanding this deeply
- Debugging an async app that "hangs" — usually one blocking call is freezing everything.
- Choosing libraries: you must pick async-native clients (`httpx`, `asyncpg`, `aioredis`) so they yield properly.
- Offloading CPU work: wrap blocking calls in `asyncio.to_thread(...)` so they run in a thread and do not freeze the loop.

---

## Theory Chapter 3: `gather` vs `create_task` — two ways to run concurrently

### 3.1 The mental distinction
- `asyncio.gather(...)` = "run this whole batch together and give me all results when everyone finishes." It is fire-and-collect.
- `asyncio.create_task(...)` = "start this one job running in the background *right now* and hand me a handle I can check, cancel, or await later." It is fire-and-manage.

### 3.2 `asyncio.gather` — batch fan-out / fan-in
```python
import asyncio

async def fetch(n):
    await asyncio.sleep(n)
    return f"result-{n}"

async def main():
    # All three start immediately; gather waits for ALL to finish.
    results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
    print(results)  # ['result-1', 'result-2', 'result-3'] — input order preserved

asyncio.run(main())
```
Key properties:
- Results come back in **input order**, not completion order.
- Elapsed time = the **slowest** task (here ~3s), not the sum.
- If one task raises, by default `gather` propagates that exception (use `return_exceptions=True` to collect errors instead of raising).

Real-world analogy: sending 3 friends to 3 shops with one shopping list each, then waiting at the entrance until *all* return before leaving together.

### 3.3 `asyncio.create_task` — individual lifecycle control
```python
import asyncio

async def fetch(n):
    await asyncio.sleep(n)
    return f"result-{n}"

async def main():
    task = asyncio.create_task(fetch(3))  # starts running NOW

    # ... you can do other work here while the task runs ...
    await asyncio.sleep(0.5)

    if not task.done():
        print("still running, I could cancel it if needed")

    result = await task  # await it whenever you're ready
    print(result)

asyncio.run(main())
```
Key properties:
- The coroutine begins executing the moment you call `create_task`.
- You get a `Task` object you can `.cancel()`, attach `.add_done_callback(...)`, or `await` later.
- Ideal for background jobs and long-lived work.

Real-world analogy: starting the washing machine and keeping the timer card in your pocket. You go do other chores; you check or stop it whenever you want.

### 3.4 Decision rule (memorize this)
| Situation | Use |
|---|---|
| Run a batch, want all results together | `gather` |
| Need results in one aggregated list | `gather` |
| Launch now, await later | `create_task` |
| Might cancel it mid-flight | `create_task` |
| Attach a completion callback | `create_task` |
| Background job outliving the current function | `create_task` |

### 3.5 Common mistakes
1. **Forgetting to await a task** — `create_task(...)` without ever awaiting it can let the program exit before it finishes, or swallow its exception silently.
2. **Calling a coroutine without scheduling it** — `fetch(3)` alone does nothing; it must be inside `gather`, `create_task`, or `await`.
3. **Expecting completion order from gather** — gather preserves *input* order; if you need "first done first," use `asyncio.as_completed`.

---

## Theory Chapter 4: Bounded concurrency — the most important production skill

### 4.1 Why unbounded concurrency is dangerous
"Just launch all 10,000 requests at once" feels fast but breaks real systems:
- **API rate limits** — the server returns 429 and bans you.
- **Socket / file-descriptor exhaustion** — the OS runs out of connections.
- **Memory pressure** — 10,000 in-flight responses buffered at once.
- **Cascading failure** — you overwhelm a downstream service and take it down, which takes *you* down.

### 4.2 Real-world analogy: the nightclub with a bouncer
A club (the downstream API) safely holds 50 people. Without a bouncer, 5,000 people rush the door — injuries, chaos, the club shuts down. A bouncer (`Semaphore`) lets exactly 50 in; as one leaves, one enters. The club stays healthy and the line still moves quickly.

### 4.3 How a Semaphore works
A `Semaphore(K)` is a counter starting at K. `async with sem:` decrements it on entry and increments on exit. If the counter is 0, new arrivals *wait* until someone leaves.

```python
import asyncio

async def worker(sem: asyncio.Semaphore, n: int):
    async with sem:              # wait here if K workers already inside
        print(f"worker {n} entered")
        await asyncio.sleep(1)   # simulated I/O
        print(f"worker {n} leaving")

async def main():
    sem = asyncio.Semaphore(3)   # at most 3 inside at once
    await asyncio.gather(*(worker(sem, i) for i in range(9)))

asyncio.run(main())
```
With 9 workers and `Semaphore(3)`, they run in 3 waves of 3. Total time ≈ 3 seconds instead of 1 (unbounded) — you trade a little speed for a lot of safety.

### 4.4 The throughput formula
$$\text{elapsed} \approx \left\lceil \frac{\text{tasks}}{\text{concurrency}} \right\rceil \times \text{avg\_task\_time}$$

- concurrency = 1 → behaves like sequential
- concurrency = tasks → behaves like unbounded (all at once)
- somewhere in between → the sweet spot that is fast *and* stable

### 4.5 How to tune the limit (practical method)
1. Start conservative: `K = 3` to `10`.
2. Measure two things: total elapsed time and failure rate (and p95 latency if you can).
3. Increase `K` gradually.
4. **Stop increasing** the moment failures rise or latency gets worse. That inflection point is your ceiling; back off slightly from it.

The goal is not maximum concurrency. It is the highest concurrency that stays reliable.

### 4.6 Use cases
- Bulk-calling any external API (the everyday case).
- Web scrapers that must respect a site's capacity.
- Batch LLM calls where the provider enforces tokens/requests per minute.
- Database write fan-out where the pool has limited connections.

### 4.7 Common mistakes
1. Creating a new `Semaphore` *inside* each task instead of sharing one — gives no limiting at all.
2. Setting `K` too high "for speed" and getting mass 429/500 errors that are slower overall after retries.
3. Forgetting that retries multiply load — a semaphore of 10 with retries can still spike well above 10 effective requests.

---

## Practical lab (today)
File: `src/weeks/week_02/foundations/session1_concurrency_deepening.py`

Run:
```bash
python src/weeks/week_02/foundations/session1_concurrency_deepening.py
```

What to observe:
1. Sequential elapsed time
2. Concurrent (unbounded) elapsed time
3. Concurrent with semaphore limits (2, 4, 8)
4. Throughput trade-off table

---

## Assignment
1. Add one more experiment with semaphore limit `1` and explain why it approximates sequential.
2. Add one experiment with limit `12` and compare failure behavior (if any).
3. Add an analysis paragraph:
- Which limit gives best balance between speed and stability in your run?
- Why that limit and not max possible?

## Evidence to submit
1. Terminal output from the lab script
2. Your chosen best semaphore limit + reasoning
3. Updated code snippet showing added experiments

## Quiz (answer after you run)
1. Why can concurrency reduce total elapsed time even if each request takes the same per-request latency?
2. Why is `time.sleep()` harmful inside async code?
3. When should you prefer `create_task` over `gather`?
4. What production risk does a semaphore protect against?
5. If increasing concurrency from 4 to 12 makes failures rise, what do you do and why?

---

## Revision note
- Concurrency overlaps waiting; it does not magically speed up compute.
- Event loop fairness depends on cooperative yielding at `await` points.
- `gather` is for batch aggregation, `create_task` is for lifecycle control.
- Semaphore is the core guardrail for safe real-world concurrency.
