# Week 2 | Session 2: Failure Isolation and Resilient Concurrency

## Session goal
Move from "my concurrent code works when everything succeeds" to "my concurrent code stays correct, safe, and predictable when some tasks fail, hang, or must be cancelled."

## Where we are in roadmap
- Phase 1 (Weeks 2–4): production-grade async and resilience patterns
- Session 1: concurrency internals, gather vs create_task, bounded concurrency
- **This session:** failure isolation, exception handling in batches, streaming results, cancellation, and a robust runner that combines semaphore + timeout + retry

## Prerequisites
- Week 2 Session 1 lab runs cleanly
- Environment active: `source .venv/bin/activate`
- Python 3.9 (we deliberately avoid `asyncio.TaskGroup`, which needs 3.11+, and teach the patterns that work everywhere)

---

## How to use this document
Read each chapter top to bottom. Every concept has:
1. Plain-language explanation (what it is and why it matters)
2. Real-world analogy (to build intuition)
3. Code example (exact syntax)
4. Use cases (when you actually reach for it)
5. Common mistakes (what goes wrong and why)

Run the lab file while reading. Observe the numbers and behavior, then re-read the theory.

---

## Theory Chapter 1: What "failure isolation" means

### 1.1 Plain-language explanation
When you run many tasks concurrently, some will fail — a network blip, a bad input, a slow server. **Failure isolation** means one task's failure does not silently corrupt your results or crash the whole batch. Each task's outcome (success *or* failure) is captured, labelled, and handled deliberately.

The opposite — "failure contagion" — is when a single exception aborts the entire batch and you lose the results of the tasks that *did* succeed.

### 1.2 Real-world analogy: a delivery company
You dispatch 100 delivery drivers in the morning. Two get flat tires. A well-run company does not cancel all 100 deliveries because two failed — it records "2 failed, 98 delivered," reschedules the two, and keeps the good results. A badly-run company loses track of everything the moment one driver has trouble.

Failure isolation is running the batch like the well-run company: **partial failure is normal and accounted for, not catastrophic.**

### 1.3 Why this matters more in async
In synchronous loops you naturally handle each item in its own `try/except`. In concurrent code, all tasks are "in flight" at once, so you need explicit tools to collect per-task outcomes without letting the first exception unwind everything.

### 1.4 The mental model
Think of every concurrent task as returning one of two things:
- a **result** (it succeeded), or
- an **error** (it failed, but the error is *data* you can inspect, not an explosion).

Your job is to design the batch so both outcomes are first-class.

### 1.5 Common mistake
Assuming "if it ran in testing, all tasks will succeed in production." At scale, some fraction *always* fails. Design for a non-zero failure rate from day one.

---

## Theory Chapter 2: `gather(return_exceptions=True)` — the isolation switch

### 2.1 Plain-language explanation
By default, `asyncio.gather(...)` is "fail-fast": the moment any task raises, `gather` re-raises that exception to you and you lose easy access to the other results. Passing `return_exceptions=True` flips this: instead of raising, gather **returns the exception object in the results list**, in the same position as that task. Now you get every outcome, good and bad, in one list.

### 2.2 Real-world analogy: a group exam
- **Default gather (fail-fast):** the teacher grades papers and the instant one student fails, they stop grading entirely and throw out the whole pile. You never learn how everyone else did.
- **`return_exceptions=True`:** the teacher grades every paper and hands back the full stack — some marked "pass," some marked "fail" — so you can see the complete picture.

### 2.3 Code example
```python
import asyncio

async def task(n):
    await asyncio.sleep(0.1)
    if n == 3:
        raise ValueError(f"task {n} failed")
    return f"result-{n}"

async def main():
    coros = [task(i) for i in range(5)]
    results = await asyncio.gather(*coros, return_exceptions=True)

    for i, r in enumerate(results):
        if isinstance(r, Exception):
            print(f"task {i}: FAILED ({type(r).__name__}: {r})")
        else:
            print(f"task {i}: OK -> {r}")

asyncio.run(main())
```
Output: tasks 0,1,2,4 report OK; task 3 reports FAILED — and the batch still completes.

### 2.4 The golden rule
When you use `return_exceptions=True`, you **must** inspect the results and check `isinstance(r, Exception)`. The exceptions are now silent data — if you forget to check, you will treat an error object as if it were a valid result.

### 2.5 Use cases
- Health-checking many endpoints where some are expected to be down.
- Bulk API calls where partial success is acceptable and you want a success/failure report.
- Any "process this whole batch and tell me what worked" job.

### 2.6 Common mistakes
1. Forgetting the `isinstance` check and passing an exception object downstream as data.
2. Using `return_exceptions=True` when you actually want fail-fast (e.g., a transaction where any failure should abort everything). Pick the mode intentionally.
3. Losing *which* input failed — always keep the index or the input alongside the result so you can retry or report it.

---

## Theory Chapter 3: `as_completed` — react as results arrive

### 3.1 Plain-language explanation
`gather` gives you everything at the end, in input order. `asyncio.as_completed` gives you results **one at a time, in the order they finish**. You can start processing the fast responses immediately instead of waiting for the slowest one.

### 3.2 Real-world analogy: a pizza kitchen with a pickup counter
`gather` is "we hold all the pizzas until every order is done, then release them together." `as_completed` is "each pizza goes to the counter the moment it's ready." Customers with quick orders don't wait behind the one complicated order.

### 3.3 Code example
```python
import asyncio

async def task(n, delay):
    await asyncio.sleep(delay)
    return f"result-{n} (took {delay}s)"

async def main():
    coros = [task(1, 0.3), task(2, 0.1), task(3, 0.2)]
    for future in asyncio.as_completed(coros):
        result = await future        # yields in FINISH order: 2, 3, 1
        print("ready:", result)

asyncio.run(main())
```

### 3.4 Use cases
- Streaming partial results to a UI or log as soon as each is ready.
- "First good answer wins" patterns (though `asyncio.wait(..., return_when=FIRST_COMPLETED)` can be cleaner for that).
- Long-running batches where early feedback matters.

### 3.5 Common mistakes
1. Expecting input order — `as_completed` yields in *completion* order by design.
2. Losing track of which input a result belongs to — the finish order scrambles it, so embed an id inside each task's return value.
3. Forgetting to `await future` inside the loop.

---

## Theory Chapter 4: Timeouts on concurrent work

### 4.1 Plain-language explanation
A timeout caps how long you'll wait for an operation. If it exceeds the limit, it is cancelled and raises `asyncio.TimeoutError`. In a batch, a per-task timeout prevents one stuck task from holding a concurrency slot forever and starving the rest.

### 4.2 Real-world analogy: a timed exam question
You give yourself 2 minutes per question. If one question is impossible, you don't spend the whole exam on it — the timer forces you to move on so the other questions still get answered.

### 4.3 Per-task timeout (the pattern that scales)
Wrap each individual task, not the whole batch, so a single slow task fails alone instead of killing everything:
```python
import asyncio

async def guarded(coro, timeout):
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return TimeoutError(f"exceeded {timeout}s")

async def main():
    tasks = [guarded(work(i), timeout=1.0) for i in range(5)]
    results = await asyncio.gather(*tasks)   # each task self-limits
    ...

asyncio.run(main())
```

### 4.4 Use cases
- Every network/DB/LLM call in a batch (a hanging call is worse than a failed one).
- SLA enforcement — "no single item may take more than X seconds."

### 4.5 Common mistakes
1. Putting the timeout only around the *whole* `gather` — one slow task can still consume the entire budget and cancel healthy tasks.
2. Never setting a timeout and relying on a library default of "wait forever."
3. Setting the timeout shorter than a task's normal duration, causing false failures.

---

## Theory Chapter 5: Cancellation and `CancelledError`

### 5.1 Plain-language explanation
Cancellation is asking a running task to stop. Async does this by raising `asyncio.CancelledError` *inside* the task at its next `await`. Well-behaved tasks let it propagate (so they actually stop) but may run cleanup first. Cancellation is cooperative — a task only stops at an `await` point.

### 5.2 Real-world analogy: recalling a search party
You've sent searchers into the field. You radio "come back" (cancel). They don't teleport home — they finish their current step, pack up their gear (cleanup), and return. If a searcher ignores the radio and keeps going, they were "swallowing the cancellation," which is a bug.

### 5.3 Code example
```python
import asyncio

async def worker():
    try:
        while True:
            await asyncio.sleep(0.5)
            print("working...")
    except asyncio.CancelledError:
        print("cleanup before stopping")
        raise          # re-raise so cancellation completes

async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(1.2)
    task.cancel()                       # request cancellation
    try:
        await task                      # wait for it to actually stop
    except asyncio.CancelledError:
        print("worker cancelled cleanly")

asyncio.run(main())
```

### 5.4 Use cases
- Stopping background jobs on shutdown.
- "First result wins": cancel the losers once a winner arrives.
- Aborting work when a client disconnects or a deadline passes.

### 5.5 Common mistakes
1. **Swallowing `CancelledError`** — catching it and *not* re-raising means the task refuses to stop. Only catch it to clean up, then `raise`.
2. Doing heavy `await` work inside the `except CancelledError` block — cleanup should be quick.
3. Forgetting to `await task` after `.cancel()`, so you don't actually wait for it to finish stopping.

---

## Theory Chapter 6: The robust runner — combining every guardrail

### 6.1 Plain-language explanation
Real production batch processors layer four things together:
1. **Semaphore** — cap concurrency (safety, from Session 1).
2. **Timeout** — no single task hangs forever.
3. **Retry** — transient failures get another chance (from Week 1 Session 2).
4. **Isolation** — collect all outcomes; one failure never aborts the batch.

Stacked correctly, they turn a fragile "hope it works" loop into a predictable, tunable, self-reporting system.

### 6.2 Real-world analogy: an air traffic control tower
- Semaphore = only N planes on approach at once.
- Timeout = a plane that can't land in its window is waved off.
- Retry = the waved-off plane circles and tries again.
- Isolation = one diverted flight doesn't ground the whole airport; every flight's status is tracked on the board.

### 6.3 The ordering that matters (inside-out)
The layers nest in a specific order:
```
semaphore  ->  retry  ->  timeout  ->  the actual work
```
- The **semaphore** is outermost so retries and waits still count against your concurrency budget (a retrying task keeps holding its slot).
- **Retry** wraps **timeout** so each individual attempt is time-bounded and a timeout can *trigger* a retry.
- The **timeout** is closest to the work so it limits one attempt, not the whole retry chain.

### 6.4 Code sketch (see the lab for the full version)
```python
import asyncio
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

class TransientError(RuntimeError):
    ...

@retry(
    retry=retry_if_exception_type((TransientError, asyncio.TimeoutError)),
    wait=wait_exponential(multiplier=0.1, min=0.1, max=1.0),
    stop=stop_after_attempt(3),
)
async def attempt(n, timeout):
    return await asyncio.wait_for(do_work(n), timeout=timeout)

async def run_one(sem, n, timeout):
    async with sem:                          # concurrency cap (outermost)
        try:
            return {"id": n, "ok": True, "value": await attempt(n, timeout)}
        except Exception as exc:             # isolation: capture, don't crash
            return {"id": n, "ok": False, "error": f"{type(exc).__name__}: {exc}"}

async def run_batch(items, concurrency, timeout):
    sem = asyncio.Semaphore(concurrency)
    results = await asyncio.gather(*(run_one(sem, n, timeout) for n in items))
    return results
```

### 6.5 Use cases
- Bulk LLM inference with provider rate limits + occasional 429s.
- Mass web scraping with flaky endpoints.
- Any "process N items reliably and give me a success/failure report" job.

### 6.6 Common mistakes
1. Wrapping the timeout *around the whole retry* by accident, so backoff waits eat the timeout budget (see Week 1 Session 2, Chapter 5).
2. Retrying non-transient errors (a 401 or a `ValueError` from bad input) — wasted attempts.
3. Not returning a structured per-item outcome, so you can't tell *which* items failed or feed them into a retry queue.

---

## Practical lab (today)
File: `src/weeks/week_02/foundations/session2_resilient_concurrency.py`

Run:
```bash
python src/weeks/week_02/foundations/session2_resilient_concurrency.py
```

What to observe:
1. **Demo 1 — isolation:** a batch where some tasks fail; `return_exceptions=True` keeps the good results.
2. **Demo 2 — as_completed:** results printed in finish order, not input order.
3. **Demo 3 — per-task timeout:** a slow task fails alone while others succeed.
4. **Demo 4 — cancellation:** a worker is cancelled and cleans up before stopping.
5. **Demo 5 — robust runner:** semaphore + timeout + retry + isolation, with a final success/failure summary.

---

## Assignment
1. In the robust runner, change `concurrency` from 3 to 1 and to 10; record the elapsed time and failure count for each.
2. Add a **permanent** error type (e.g. `PermanentError(RuntimeError)`) that is NOT retried, raise it for one item, and confirm it fails immediately (no retries) while transient failures still retry.
3. Add an analysis paragraph:
   - How many items succeeded, failed transiently-then-recovered, and failed permanently?
   - What concurrency gave the best balance of speed and reliability, and why?

## Evidence to submit
1. Terminal output of all five demos
2. Your success/failure summary table from the robust runner at concurrency 1, 3, and 10
3. Your code snippet adding the permanent-error path
4. Your analysis paragraph

## Quiz (answer after you run)
1. What is the difference between default `gather` and `gather(return_exceptions=True)`?
2. After using `return_exceptions=True`, what check must you never forget?
3. Why does `as_completed` scramble the order, and how do you keep track of which result is which?
4. Why is a per-task timeout better than one timeout around the whole batch?
5. Why must you re-raise `CancelledError` after cleaning up?
6. In the robust runner, why is the semaphore the outermost layer and the timeout the innermost?

---

## Revision note
- **Failure isolation** = one task's failure never aborts the batch; every outcome is captured as data.
- `gather(return_exceptions=True)` returns exceptions in place — always `isinstance`-check the results.
- `as_completed` yields in finish order; embed an id so you know which result is which.
- **Per-task timeouts** stop one hung task from starving the whole batch.
- **Cancellation** is cooperative: catch `CancelledError` only to clean up, then re-raise.
- The **robust runner** nests guardrails inside-out: `semaphore -> retry -> timeout -> work`.
- Retry only **transient** errors; fail fast on permanent ones. Always return a structured per-item outcome.
