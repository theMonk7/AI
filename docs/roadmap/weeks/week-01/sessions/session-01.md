# Week 1 Session 1: Async Python Fundamentals

## Session goal
Understand how async code works in Python from first principles, and apply it to concurrent API-style tasks with full confidence about *why* it works.

## Prerequisites
- Setup completed from docs/setup/environment_setup.md
- Virtual environment activated

## How to use this document
Every concept below is taught in the mastery format:
1. Plain-language explanation (what it is, why it matters)
2. Real-world analogy (to build intuition)
3. Code example (exact syntax)
4. Use cases (when to reach for it)
5. Common mistakes (what breaks and why)

---

## Theory Chapter 1: Coroutines — the `async def` function

### 1.1 Plain-language explanation
A coroutine is a special function defined with `async def`. The critical surprise for beginners: **calling it does not run it.** It hands you back a "coroutine object" — a to-do ticket that describes work to be done later. The work only happens when you `await` it or schedule it on the event loop.

### 1.2 Real-world analogy: ordering at a restaurant
Writing `async def cook_pasta()` is like printing a recipe card. Calling `cook_pasta()` is like handing that card to the kitchen — you now hold an *order ticket*, but no pasta exists yet. Only when the kitchen actually *works the ticket* (`await`) does food get cooked.

### 1.3 Code example
```python
import asyncio

async def cook_pasta():
    await asyncio.sleep(1)   # simulate cooking time
    return "pasta ready"

ticket = cook_pasta()        # NOTHING cooks — this is just a coroutine object
print(ticket)                # <coroutine object cook_pasta at 0x...>

async def main():
    dish = await ticket      # NOW it actually runs
    print(dish)              # "pasta ready"

asyncio.run(main())
```

### 1.4 Use cases
Any function that *waits* on something external: HTTP requests, database queries, file I/O, LLM API calls, message queues. Declaring these `async def` lets them yield control while waiting.

### 1.5 Common mistake
Calling a coroutine and forgetting to await it. `cook_pasta()` on its own silently does nothing and Python may warn "coroutine was never awaited." The food never gets cooked.

---

## Theory Chapter 2: `await` — pause and resume

### 2.1 Plain-language explanation
`await` means: "start this work, and while it is waiting, let the event loop go do other useful things; wake me up when it is done." It is the single point where a coroutine voluntarily gives up control.

### 2.2 Real-world analogy: microwaving while cooking
You put food in the microwave and press start (`await`). Instead of standing frozen watching it, you turn to chop vegetables. When the microwave beeps, you come back and continue. `await` is you saying "I'll step away during this wait."

### 2.3 Code example
```python
import asyncio

async def task(name, seconds):
    print(f"{name}: started")
    await asyncio.sleep(seconds)   # yields control here
    print(f"{name}: finished after {seconds}s")

async def main():
    await asyncio.gather(task("A", 2), task("B", 1))

asyncio.run(main())
# A starts, B starts, B finishes (1s), A finishes (2s) — total ~2s not 3s
```

### 2.4 Use cases
Put `await` before every coroutine call or async I/O operation: `await client.get(url)`, `await db.fetch(query)`, `await asyncio.sleep(t)`.

### 2.5 Common mistake
Awaiting things sequentially when they could overlap. `await a()` then `await b()` runs them one after another. To overlap, hand both to `gather`.

---

## Theory Chapter 3: The event loop — the scheduler

### 3.1 Plain-language explanation
The event loop is a single-threaded manager that keeps a list of coroutines and runs them one at a time, switching between them at each `await`. It is not parallel execution — it is extremely fast juggling of paused-and-resumed work.

### 3.2 Real-world analogy: a receptionist at a busy desk
One receptionist (the loop) serves many visitors (coroutines). They help visitor A until A needs to fill out a form (`await`). Instead of watching A write, they help visitor B, then C. When A's form is ready, they return to A. One person, everyone served efficiently.

### 3.3 Code example
```python
import asyncio

async def main():
    print("loop running my coroutine")

asyncio.run(main())   # creates the loop, runs main(), then shuts the loop down
```

### 3.4 Use cases
`asyncio.run(main())` is the standard entry point of any async program. It is called exactly once at the top level.

### 3.5 Common mistake
Calling `asyncio.run()` more than once in a program, or calling it inside an already-running loop (raises `RuntimeError: asyncio.run() cannot be called from a running event loop`). Inside async code, use `await`, not another `asyncio.run()`.

---

## Theory Chapter 4: Sequential vs concurrent execution

### 4.1 Plain-language explanation
Sequential = each task waits for the previous one to finish. Concurrent = tasks are started together and their *waiting times overlap*. Concurrency only helps when tasks spend time waiting (I/O), not computing.

### 4.2 Real-world analogy: laundry
Three loads of laundry. Sequential: wash load 1, wait, dry it, then start load 2. Concurrent: start washer *and* dryer running different loads at once. The waiting overlaps, so all loads finish sooner — but you did not make any single machine faster.

### 4.3 Code example
```python
import asyncio, time

async def fetch(n):
    await asyncio.sleep(1)   # 1 second of "waiting"
    return n

async def sequential():
    start = time.perf_counter()
    for i in range(3):
        await fetch(i)       # one at a time → ~3s
    print("sequential:", round(time.perf_counter() - start, 1))

async def concurrent():
    start = time.perf_counter()
    await asyncio.gather(*(fetch(i) for i in range(3)))  # overlap → ~1s
    print("concurrent:", round(time.perf_counter() - start, 1))

asyncio.run(sequential())
asyncio.run(concurrent())
```

### 4.4 Use cases
Fanning out to many independent endpoints, running multiple DB queries, checking many URLs — anything where tasks are independent and I/O-bound.

### 4.5 Common mistake
Expecting concurrency to speed up CPU-heavy work (math, hashing). There is no wait to overlap there, so async gives no benefit — you need multiprocessing instead.

---

## Theory Chapter 5: `asyncio.gather` — run a batch together

### 5.1 Plain-language explanation
`gather` takes multiple coroutines, starts them all, and returns all their results once every one has finished. Results come back in the same order you passed them, regardless of who finished first.

### 5.2 Real-world analogy: sending three friends shopping
You send three friends to three stores simultaneously and wait at the car. You leave together only when all three return. You get their bags back in the order you assigned them, not the order they returned.

### 5.3 Code example
```python
import asyncio

async def fetch(n):
    await asyncio.sleep(n)
    return f"result-{n}"

async def main():
    results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
    print(results)   # ['result-1', 'result-2', 'result-3'] — input order

asyncio.run(main())
```

### 5.4 Use cases
The default pattern for concurrent I/O: multiple API calls, parallel reads, batch processing where you want all results collected together.

### 5.5 Common mistake
Assuming results arrive in completion order. They do not — gather preserves input order. If one coroutine raises, gather propagates the exception (unless you pass `return_exceptions=True`).

---

## Theory Chapter 6: `asyncio.create_task` — launch and manage

### 6.1 Plain-language explanation
`create_task` schedules a coroutine to start running immediately in the background and hands you a `Task` handle. With that handle you can check if it's done, cancel it, attach a callback, or await it later.

### 6.2 Real-world analogy: starting a dishwasher
You load and start the dishwasher (`create_task`) and keep going about your evening. You hold a mental note that it's running. You can stop it early, or wait for it to finish whenever you choose.

### 6.3 Code example
```python
import asyncio

async def slow_job():
    await asyncio.sleep(2)
    return "done"

async def main():
    task = asyncio.create_task(slow_job())  # starts NOW
    print("doing other work while it runs...")
    result = await task                     # collect result later
    print(result)

asyncio.run(main())
```

### 6.4 Use cases
Background jobs, work you might cancel, tasks needing completion callbacks, or when you want to start something now and await it after doing other work.

### 6.5 Common mistake
Creating a task and never awaiting it — the program may exit before it finishes, and any exception it raised gets swallowed silently.

---

## Theory Chapter 7: `asyncio.Semaphore` — cap concurrency

### 7.1 Plain-language explanation
A semaphore limits how many coroutines can be inside a protected block at once. If the limit is 3, the fourth coroutine waits until one of the three finishes. It is the guardrail that keeps concurrency safe.

### 7.2 Real-world analogy: three fitting rooms in a store
A store has 3 fitting rooms. However many shoppers show up, only 3 try clothes at a time; the rest queue. As one leaves, the next enters. This protects the store from chaos while the line still moves.

### 7.3 Code example
```python
import asyncio

async def worker(sem, n):
    async with sem:                 # wait if 3 already inside
        await asyncio.sleep(1)
        return n

async def main():
    sem = asyncio.Semaphore(3)      # at most 3 at once
    await asyncio.gather(*(worker(sem, i) for i in range(9)))  # 3 waves

asyncio.run(main())
```

### 7.4 Use cases
Bulk-calling any external API (to respect rate limits), web scraping, batch LLM calls, and any fan-out to a service with limited capacity.

### 7.5 Common mistake
Creating a fresh `Semaphore` inside each task instead of sharing one instance — that provides no limiting at all. The semaphore must be created once and passed to every worker.

---

## Run examples
1. Run all examples:
   python src/weeks/week_01/foundations/module1_session1_async.py

2. Observe output sections:
- Example 1: coroutine basics
- Example 2: sequential vs concurrent timing
- Example 3: gather and create_task
- Example 4: semaphore-limited worker pool
- Mini project: async endpoint simulation report

## Real API lab included in this session
The same script now runs live public API workflows for:
1. Serial calls
2. Parallel calls
3. Dependency chain calls
4. Done callbacks
5. Cancellation
6. Semaphore-limited concurrency

Use this as your real-task simulation baseline.

## Concept to code mapping
1. Serial pattern:
- Function: serial_live_calls
- Learning: deterministic order, higher elapsed time.

2. Parallel pattern:
- Function: parallel_live_calls
- Learning: overlap network waiting with gather.

3. Dependency pattern:
- Function: dependency_live_calls
- Learning: second call depends on data from first call (userId).

4. Done callback pattern:
- Function: done_callback_calls
- Learning: observe completion order independent of submission order.

5. Cancellation pattern:
- Function: cancellation_calls
- Learning: cancel long-running tasks and handle CancelledError cleanly.

6. Semaphore pattern:
- Function: semaphore_live_calls
- Learning: cap in-flight concurrency to protect APIs and your app.

## Guided exercise flow
1. Run once and capture baseline elapsed times for each pattern.
2. Change semaphore limit from 2 to 3 and rerun.
3. Replace one URL with a slower endpoint and observe completion order.
4. In cancellation_calls, increase sleep before cancel from 1.0 to 2.0 and compare results.
5. Summarize tradeoffs: fastest vs safest vs most controllable pattern.

## Assignment for this session
1. Change worker concurrency from 3 to 2 and compare elapsed time.
2. Add two fake endpoints to the mini-project list.
3. Re-run and record what changes.

## Evidence to save
- Terminal output screenshot or log
- Notes on why concurrent elapsed time improved
- One paragraph on where async helps and where it does not

## Common mistakes
- Calling async function without await
- Mixing blocking time.sleep inside async functions
- Creating too many concurrent tasks without limits

## Revision note (end of session)
- You learned what `async def` creates: a coroutine that runs when awaited or scheduled.
- You used `await` to pause one task while the event loop runs others.
- You compared serial and parallel API calls and measured latency differences.
- You implemented dependency chaining where call 2 depends on data from call 1.
- You used `create_task` and done callbacks to observe completion order.
- You implemented cancellation and handled `CancelledError` safely.
- You applied `Semaphore` to cap concurrency and protect API usage.
