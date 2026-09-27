# Week 2 | Session 3: Async Pipelines — Queues, Worker Pools & Rate Limiting

## Session goal
Move from "I can run a batch of concurrent tasks" to "I can build a continuous, backpressure-aware async pipeline that streams work through a pool of workers at a controlled rate" — the shape of every real scraper, ingester, and data pipeline.

## Where we are in roadmap
- Phase 1 (Weeks 1–3): production-grade async and resilience
- Session 1: concurrency internals, gather vs create_task, bounded concurrency
- Session 2: failure isolation, timeouts, cancellation, the robust runner
- **This session:** `asyncio.Queue`, the producer–consumer pattern, worker pools, rate limiting, and graceful shutdown — then the **Week 2 cumulative project**

## Prerequisites
- Week 2 Sessions 1–2 labs run cleanly
- Environment active: `source .venv/bin/activate`
- Python 3.9 (we avoid `TaskGroup`; all patterns here work on 3.9)

---

## How to use this document
Every concept is taught in the mastery format:
1. Plain-language explanation
2. Real-world analogy
3. Code example
4. Use cases
5. Common mistakes

Run the lab while reading. Watch the workers pull items and the rate limiter pace them.

---

## Theory Chapter 1: Why `gather` isn't always enough

### 1.1 Plain-language explanation
`gather` is perfect when you have a **fixed, known list** of tasks and want them all done. But real systems often have work that **arrives over time** (new URLs discovered while crawling, messages landing on a webhook, rows streaming from a file too big for memory). For that you need a **pipeline**: one part *produces* work, another part *consumes* it, and a buffer sits between them. That buffer is a queue.

### 1.2 Real-world analogy: a restaurant kitchen
`gather` is a catering order: "make exactly these 50 dishes." A pipeline is a working restaurant: orders (work) keep arriving through the evening, a line of cooks (workers) pull tickets from a rail (the queue) as fast as they can, and the rail holds tickets when cooks are busy. Nobody knows the full night's orders in advance — the system just keeps flowing.

### 1.3 The pipeline shape
```
producer(s) ──put──▶ [ asyncio.Queue ] ──get──▶ worker pool ──▶ results
```
- **Producer:** discovers/creates work and `put`s it on the queue.
- **Queue:** a thread-safe (task-safe) buffer that decouples the two sides.
- **Workers:** a fixed number of coroutines that loop, `get` an item, process it, repeat.


**Execution Order:**
```
 
Start consumer
      │
      ▼
Consumer waiting on queue.get()

      │
      ▼
Producer adds Job 1
      │
      ▼
Consumer immediately gets Job 1

Producer adds Job 2
      │
      ▼
Consumer gets Job 2

Producer adds Job 3
      │
      ▼
Consumer gets Job 3
```

### 1.4 Use cases
Web scrapers/crawlers, file/DB ingestion pipelines, message/webhook processors, batch LLM/embedding jobs where items stream in, ETL jobs.

### 1.5 Common mistake
Reaching for `gather` when work arrives dynamically, then rebuilding the list and re-calling `gather` in a loop. That is clumsy and loses backpressure. A queue + worker pool is the right tool.

---

## Theory Chapter 2: `asyncio.Queue` — the buffer between stages

### 2.1 Plain-language explanation
`asyncio.Queue` is a first-in-first-out buffer designed for coroutines. Producers `await queue.put(item)` to add work; consumers `await queue.get()` to take it. Crucially, both operations can **wait**: `get` sleeps if the queue is empty (no busy-looping), and `put` sleeps if the queue is *full* (when you set a `maxsize`). That waiting is how the queue provides **backpressure**.

### 2.2 Real-world analogy: a conveyor belt with limited length
The queue is a conveyor belt between two workstations. If the belt is empty, the downstream worker waits for the next item to arrive. If the belt is full (bounded length), the upstream worker must pause loading until space frees up — this stops a fast producer from burying a slow consumer.

### 2.3 Code example
```python
import asyncio

async def main():
    queue: asyncio.Queue = asyncio.Queue(maxsize=5)  # bounded → backpressure

    await queue.put("job-1")     # add work
    await queue.put("job-2")
    print("size:", queue.qsize())  # 2

    item = await queue.get()     # take work (waits if empty)
    print("got:", item)
    queue.task_done()            # tell the queue this item is finished

asyncio.run(main())
```

### 2.4 The four methods that matter
| Method | Meaning |
|---|---|
| `await queue.put(x)` | add item; waits if full (`maxsize` reached) |
| `await queue.get()` | remove item; waits if empty |
| `queue.task_done()` | signal that a `get`-ten item is fully processed |
| `await queue.join()` | wait until every put item has had `task_done()` |

### 2.5 Use cases
Any producer–consumer setup; smoothing bursty input; bounding memory by capping `maxsize`.

### 2.6 Common mistakes
1. Forgetting `task_done()` — then `queue.join()` hangs forever waiting for a count that never reaches zero.
2. Using an **unbounded** queue for a fast producer + slow consumer — memory balloons because nothing applies backpressure.
3. Busy-waiting with `qsize()` polling instead of just `await queue.get()`.

---

## Theory Chapter 3: The worker pool

### 3.1 Plain-language explanation
A worker pool is a **fixed number of consumer coroutines** that each run the same loop: `get` an item, process it, mark it done, repeat. Because the pool size is fixed, it caps concurrency *by construction* — you don't even need a separate semaphore. Ten workers means at most ten items in flight.

### 3.2 Real-world analogy: supermarket checkout lanes
The store opens a fixed number of checkout lanes (workers). Customers (items) line up in one queue and are pulled to whichever lane is free. Ten lanes → at most ten customers being served at once, no matter how long the line grows. To handle more load you open more lanes (more workers), not infinite ones.

### 3.3 Code example
```python
import asyncio

async def worker(name, queue, results):
    while True:
        item = await queue.get()
        try:
            await asyncio.sleep(0.1)          # simulated work (I/O)
            results.append(f"{name} processed {item}")
        finally:
            queue.task_done()                 # ALWAYS, even on error

async def main():
    queue: asyncio.Queue = asyncio.Queue()
    results = []

    for i in range(20):
        queue.put_nowait(i)                   # preload work

    workers = [asyncio.create_task(worker(f"w{n}", queue, results))
               for n in range(4)]             # pool of 4

    await queue.join()                        # wait until all items processed

    for w in workers:                         # then stop the idle workers
        w.cancel()
    print(f"done: {len(results)} items by 4 workers")

asyncio.run(main())
```

### 3.4 Why the pool size *is* your concurrency limit
With N workers, exactly N items are processed at once. The throughput formula from Session 1 still applies:
$$\text{elapsed} \approx \left\lceil \frac{\text{items}}{\text{workers}} \right\rceil \times \text{avg item time}$$

### 3.5 Use cases
Crawlers, batch processors, embedding/ingestion jobs, any "many items, controlled parallelism" workload where items may arrive over time.

### 3.6 Common mistakes
1. Not putting `task_done()` in a `finally` — if processing raises, `join()` hangs.
2. Awaiting the worker tasks directly with `gather` — they loop forever; instead `await queue.join()` then cancel them.
3. Creating one task per item (that's just `gather`) instead of a fixed pool — you lose the bounded, streaming behavior.

---

## Theory Chapter 4: Graceful shutdown — draining the pipeline

### 4.1 Plain-language explanation
Workers that loop `while True` never stop on their own. You need a deliberate way to say "no more work is coming, finish what's queued, then exit." Two clean techniques: (a) `await queue.join()` then **cancel** the idle workers, or (b) put a **sentinel** value (a "poison pill") per worker that tells each one to break out of its loop.

### 4.2 Real-world analogy: closing time at the supermarket
At closing, the store stops admitting new customers but still serves everyone already in line (drain). Then each cashier, once the line is empty, closes their lane and goes home. You don't yank customers mid-checkout, and you don't leave lanes running all night.

### 4.3 Two shutdown patterns
```python
# Pattern A: join + cancel (simplest)
await queue.join()          # all items processed
for w in workers:
    w.cancel()
await asyncio.gather(*workers, return_exceptions=True)  # let cancellation settle

# Pattern B: sentinel / poison pill (one per worker)
SENTINEL = None
async def worker(queue):
    while True:
        item = await queue.get()
        if item is SENTINEL:
            queue.task_done()
            break                # this worker exits cleanly
        await do_work(item)
        queue.task_done()

for _ in workers:
    await queue.put(SENTINEL)    # exactly one stop-signal per worker
```

### 4.4 Use cases
Batch jobs that must finish and exit (Pattern A). Long-lived services that occasionally reconfigure/restart their pool (Pattern B).

### 4.5 Common mistakes
1. Cancelling workers **before** `queue.join()` — you drop unprocessed items.
2. Sending fewer sentinels than workers — some workers never get the stop signal and hang.
3. Forgetting to await the cancelled workers, so `CancelledError` surfaces as noise (recall Session 2: catch it only to clean up).

---

## Theory Chapter 5: Rate limiting — respecting external limits

### 5.1 Plain-language explanation
Concurrency limits *how many* run at once; a rate limit controls *how often* you act over time (e.g. "max 5 requests per second"). Even with only 3 workers, if each finishes in 10 ms you could fire 300 requests/second and get rate-limited (HTTP 429). A rate limiter **paces** the work — the classic model is a **token bucket**: tokens refill at a fixed rate, and each request must spend one token (waiting if the bucket is empty).

### 5.2 Real-world analogy: a toll booth that lets one car through every 2 seconds
No matter how many cars pile up (concurrency), the booth releases them at a fixed cadence. The queue can be long, cars can arrive in bursts, but the *rate* past the booth is constant and predictable — exactly what an API's "requests per second" limit expects.

### 5.3 Code example (simple async rate limiter)
```python
import asyncio, time

class RateLimiter:
    """Allow at most `rate` operations per second (simple spacing)."""
    def __init__(self, rate: float):
        self._min_interval = 1.0 / rate
        self._last = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:                       # serialize the check
            now = time.monotonic()
            wait = self._min_interval - (now - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last = time.monotonic()

async def worker(queue, limiter):
    while True:
        item = await queue.get()
        try:
            await limiter.acquire()                  # pace before the call
            await call_api(item)
        finally:
            queue.task_done()
```

### 5.4 Rate limit vs concurrency limit (they solve different problems)
| Guardrail | Controls | Protects against |
|---|---|---|
| Semaphore / worker pool | how *many* at once | overload, socket/memory exhaustion |
| Rate limiter | how *often* over time | API quotas (429), bans |
Real production clients usually need **both**.

### 5.5 Use cases
Third-party APIs with req/sec or req/min quotas, LLM provider limits, polite web scraping, paid APIs where rate = cost.

### 5.6 Common mistakes
1. Assuming a concurrency cap also caps rate — fast tasks blow past req/sec limits.
2. Rate-limiting without a lock, so many workers read the same "last time" and all fire together.
3. Ignoring the API's own `Retry-After` header (combine with the Session 2 retry/backoff).

---

## Practical lab (today)
File: `src/weeks/week_02/foundations/session3_async_pipeline.py`

Run:
```bash
python src/weeks/week_02/foundations/session3_async_pipeline.py
```

What to observe:
1. **Demo 1 — queue basics:** put/get/task_done/join lifecycle.
2. **Demo 2 — worker pool:** 4 workers draining 20 items; note the wave timing.
3. **Demo 3 — backpressure:** a bounded queue (`maxsize`) makes a fast producer wait.
4. **Demo 4 — graceful shutdown:** join + cancel, and the sentinel pattern.
5. **Demo 5 — rate limiting:** 8 workers but paced to ~5 ops/sec by the limiter.

---

## Assignment
1. Change the worker pool from 4 to 1 and to 8; record elapsed time for 20 items and explain using the throughput formula.
2. Set the queue `maxsize` very small (e.g. 2) with a fast producer and a slow consumer; describe what backpressure you observe.
3. Change the rate limiter from 5 ops/sec to 2 ops/sec; confirm the total time roughly matches `items / rate` and explain why concurrency alone couldn't achieve this.

## Evidence to submit
1. Terminal output of all five demos
2. Your throughput numbers for 1/4/8 workers
3. One paragraph: "the difference between a concurrency limit and a rate limit, in my own words"

## Quiz (answer after you run)
1. When should you use a queue + worker pool instead of `gather`?
2. What does `maxsize` on a queue give you, and why does it matter for memory?
3. Why must `task_done()` be in a `finally` block?
4. Why can you cancel idle workers only *after* `queue.join()`?
5. How many sentinels must you send to stop a pool of N workers, and why?
6. You have a 3-worker pool but still get HTTP 429 errors. What's missing and why?

---

## Revision note
- Use a **queue + worker pool** when work arrives over time or won't fit in memory; use `gather` for fixed known batches.
- `asyncio.Queue(maxsize=...)` gives **backpressure**: a bounded buffer pauses a fast producer so memory stays bounded.
- A **worker pool** of N caps concurrency by construction; `task_done()` (in `finally`) + `queue.join()` track completion.
- **Graceful shutdown:** drain with `queue.join()` then cancel, OR send one **sentinel per worker**.
- **Rate limiting** ≠ concurrency limiting: pool controls *how many*, rate limiter (token bucket) controls *how often*. Production clients usually need both, plus Session 2 retries for 429s.

---

## ▶ Next: Week 2 cumulative project
You've now finished all Week 2 teaching. Apply everything from **Weeks 1–2** in the end-of-week project:
- Brief + skeleton: `src/weeks/week_02/projects/week02_async_scraper_pipeline.py`
- It combines: async/await, `gather`, semaphores, timeouts, retries, failure isolation, queues, a worker pool, and rate limiting into one real tool.
