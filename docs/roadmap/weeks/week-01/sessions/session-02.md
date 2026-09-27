# Week 1 | Session 2: Concurrency Patterns and Reliability

## Session goal
Master bounded concurrency and fault-tolerant retry patterns that every production AI client needs, understanding *why* each pattern exists.

## Files in this session
- `src/weeks/week_01/foundations/async_patterns.py` — concurrent vs sequential benchmark
- `src/weeks/week_01/foundations/reliable_client.py` — retry, backoff, timeout

## Run commands
```bash
python src/weeks/week_01/foundations/async_patterns.py
python src/weeks/week_01/foundations/reliable_client.py
```

## How to use this document
Each concept is taught in the mastery format: plain-language explanation, real-world analogy, code example, use cases, and common mistakes.

---

## Part A: async_patterns.py — measuring concurrency

## Theory Chapter 1: Semaphore + gather (bounded concurrency)

### 1.1 Plain-language explanation
`gather` starts many coroutines at once; a `Semaphore` caps how many actually run at the same time. Combined, they let you process a large batch quickly *and* safely, without launching thousands of requests simultaneously.

### 1.2 Real-world analogy: a car wash with 3 bays
100 cars arrive (your tasks). The car wash has 3 bays (`Semaphore(3)`). All 100 cars queue up together (`gather`), but only 3 are washed at any moment. As one exits a bay, the next drives in. Fast throughput, no gridlock.

### 1.3 Code example
```python
import asyncio

semaphore = asyncio.Semaphore(3)   # allow max 3 concurrent tasks

async def task(i):
    async with semaphore:          # block until a bay is free
        await asyncio.sleep(1)
        return i

async def main():
    results = await asyncio.gather(*[task(i) for i in range(10)])
    return results

asyncio.run(main())   # 10 tasks in waves of 3 → ~4s, not 10s and not 1s
```

### 1.4 How to read the output
- Sequential elapsed ≈ sum of all individual delays.
- Concurrent elapsed ≈ `max(single task) × ceil(tasks / concurrency)`.
- The larger the task count, the bigger the win from concurrency.

### 1.5 Use cases
Batch API calls, bulk downloads, parallel database reads — any high-volume I/O where you must respect a capacity limit.

### 1.6 Common mistake
Setting concurrency too high "for speed" and triggering rate-limit errors (429) that, after retries, make the whole batch *slower*. Tune the limit; do not maximize it.

### 1.7 Experiment
Change `concurrency=3` to `concurrency=1` — concurrent elapsed equals sequential.
Change to `concurrency=10` — elapsed ≈ slowest single task only.

---

## Part B: reliable_client.py — surviving real-world failures

## Theory Chapter 2: Transient vs permanent errors

### 2.1 Plain-language explanation
Not all failures are equal. Some are temporary hiccups that will succeed if you try again (transient). Others are guaranteed to fail no matter how many times you retry (permanent). Retrying the wrong kind wastes time and money.

### 2.2 Real-world analogy: calling a friend
- **Transient:** the line is busy or the call drops. Calling again in a minute works. Worth retrying.
- **Permanent:** you dialed a disconnected number. Redialing the same wrong number a hundred times is pointless. Fix the number instead.

### 2.3 Error classification
| Error type | Example | Action |
|---|---|---|
| Transient | 503, 429, network reset, timeout | Retry with backoff |
| Permanent | 401, 404, 400 bad input | Fail immediately, do not retry |

### 2.4 Code example
```python
class TransientAPIError(RuntimeError):
    """Safe to retry — temporary condition."""

class PermanentAPIError(RuntimeError):
    """Never retry — will always fail."""
```

### 2.5 Use cases
Every external API client. Classify the response before deciding to retry, so you only spend retries where they can actually help.

### 2.6 Common mistake
Retrying a 401 Unauthorized. Your API key is wrong; retrying 4 times just delays the inevitable failure and can trip abuse detection.

---

## Theory Chapter 3: The `@retry` decorator (tenacity)

### 3.1 Plain-language explanation
`@retry` automatically re-runs a function when it raises a retryable error, waiting longer between each attempt, and giving up after a set number of tries. You declare the *policy*; tenacity handles the loop.

### 3.2 Real-world analogy: knocking on a door
No answer? Wait 1 second, knock again. Still nothing? Wait 2 seconds, knock harder. Then 4 seconds. After a few tries with growing patience, you conclude nobody's home and leave. That growing-patience pattern is exponential backoff with a stop limit.

### 3.3 Code example
```python
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

@retry(
    retry=retry_if_exception_type(TransientAPIError),
    wait=wait_exponential(multiplier=0.2, min=0.2, max=2.0),
    stop=stop_after_attempt(4),
)
async def call_api(id: str):
    ...
```

What each argument does:
- `retry_if_exception_type(TransientAPIError)` — only retry on this class (and its subclasses).
- `wait_exponential(multiplier=0.2, min=0.2, max=2.0)` — wait ~0.2s, 0.4s, 0.8s… capped at 2s.
- `stop_after_attempt(4)` — 1 original try + 3 retries = 4 total, then give up.

### 3.4 Why exponential (not constant) backoff
A struggling server needs breathing room. Constant rapid retries hammer it and prevent recovery. Doubling the wait each time gives the service progressively more time to heal.

### 3.5 Use cases
Any network call to a service that can have transient failures — third-party APIs, LLM providers, microservices, cloud storage.

### 3.6 Common mistake
Retrying without a `stop` condition — an outage could loop forever. Always cap attempts.

---

## Theory Chapter 4: Timeouts with `asyncio.wait_for`

### 4.1 Plain-language explanation
A timeout puts a hard time limit on an operation. If it does not finish in time, it is cancelled and raises `TimeoutError`. This prevents one stuck call from freezing your whole program.

### 4.2 Real-world analogy: holding on a support line
You call support and decide "I'll wait 10 minutes, then hang up." Without that limit you might wait forever, unable to do anything else. The timeout is your self-imposed hang-up rule.

### 4.3 Code example
```python
import asyncio

result = await asyncio.wait_for(call_api(id), timeout=2.5)
# Raises asyncio.TimeoutError if not done within 2.5 seconds
```

### 4.4 Use cases
Every external call must have a timeout — HTTP, DB, cache, queue. A hanging call is worse than a failed one because it consumes a slot indefinitely.

### 4.5 Common mistake
Relying on a library's default timeout (often "none"). Always set an explicit one.

---

## Theory Chapter 5: How retry + timeout interact

### 5.1 Plain-language explanation
When you wrap a retrying function in a timeout, the timeout covers the *entire* retry sequence — all attempts and all the waits between them. If the timeout is shorter than the total backoff time, it fires before the retries can finish.

### 5.2 Real-world analogy: a lunch break deadline
You'll retry knocking on a shop's door during your 30-minute lunch. But each wait between knocks grows. If your total knocking-plus-waiting exceeds 30 minutes, your lunch break (the timeout) ends first — you leave regardless of how many retries remained.

### 5.3 Worked timing example
```
Backoff between retries: 0.2 + 0.4 + 0.8 = 1.4s total
A 0.5s timeout fires before the 2nd retry can even start.
A 3.0s timeout lets all retries complete.
```

### 5.4 Use cases
Designing SLAs: you must budget timeout ≥ (sum of backoffs + sum of attempt durations), or deliberately accept early termination.

### 5.5 Common mistake
Setting timeout and retry policies independently, then being surprised when the timeout kills valid retries. Design them together as one budget.

---

## Assignment
1. In `reliable_client.py`, change `stop_after_attempt(4)` to `stop_after_attempt(2)`.
   - Run the retry-exhausted demo and observe fewer attempts.
2. Change `timeout_s=0.5` in Pattern 4 to `timeout_s=3.0`.
   - Observe that retries now complete instead of timing out.
3. Add a new error class `RateLimitError(TransientAPIError)` and raise it in some cases.
   - Verify it still retries because it inherits from `TransientAPIError`.

## Evidence to save
- Terminal output of all 4 patterns from `reliable_client.py`
- Your own words: "When should I retry, and when should I fail immediately?"

## Quiz (answer after you run)
1. Why is retrying a 401 error a waste of time?
2. Why does exponential backoff help an overloaded server more than constant retries?
3. What happens if `stop_after_attempt` is missing and the error never resolves?
4. Why must every external call have a timeout?
5. If your timeout is 0.5s and total backoff is 1.4s, what happens and why?

---

## Revision note (end of session)

- **Semaphore** limits concurrent I/O tasks to prevent overloading APIs or hitting rate limits.
- **asyncio.gather** starts all coroutines, overlaps wait times; total time ≈ slowest task not the sum.
- **Transient vs Permanent errors**: classify errors before deciding to retry. Retrying a 401 is pointless and wasteful.
- **Exponential backoff**: each retry waits longer. This gives overloaded services time to recover.
- **stop_after_attempt**: always put a hard limit on retries or you may loop indefinitely.
- **asyncio.wait_for**: every external call needs a timeout. Hanging calls are worse than failed calls.
- **Timeout + retry interact**: if timeout < total backoff time, timeout wins. Design both together.
