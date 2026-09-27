"""Week 2 | Session 2 lab: Failure Isolation and Resilient Concurrency.

Run:
    python src/weeks/week_02/foundations/session2_resilient_concurrency.py

This lab demonstrates, in order:
    1. Failure isolation with gather(return_exceptions=True)
    2. Streaming results with asyncio.as_completed (finish order)
    3. Per-task timeouts so one slow task fails alone
    4. Cooperative cancellation with clean-up
    5. A robust runner combining semaphore + retry + timeout + isolation

Python 3.9-compatible (no asyncio.TaskGroup, which needs 3.11+).
"""

from __future__ import annotations

import asyncio
import random
import time
from typing import Awaitable, Dict, List

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


# ---------------------------------------------------------------------------
# Error taxonomy (see Week 1 Session 2: transient vs permanent)
# ---------------------------------------------------------------------------
class TransientError(RuntimeError):
    """A temporary failure that is safe to retry."""


class PermanentError(RuntimeError):
    """A failure that will never succeed on retry (e.g. bad input, 401)."""


# ---------------------------------------------------------------------------
# Demo 1: failure isolation with gather(return_exceptions=True)
# ---------------------------------------------------------------------------
async def flaky_task(n: int) -> str:
    await asyncio.sleep(0.1)
    if n == 3:
        raise ValueError(f"task {n} hit bad data")
    return f"result-{n}"


async def demo_isolation() -> None:
    print("\n=== Demo 1: failure isolation (return_exceptions=True) ===")
    coros = [flaky_task(i) for i in range(5)]
    results = await asyncio.gather(*coros, return_exceptions=True)

    for i, r in enumerate(results):
        if isinstance(r, Exception):
            print(f"  task {i}: FAILED ({type(r).__name__}: {r})")
        else:
            print(f"  task {i}: OK -> {r}")
    ok = sum(1 for r in results if not isinstance(r, Exception))
    print(f"  summary: {ok}/{len(results)} succeeded, batch still completed")


# ---------------------------------------------------------------------------
# Demo 2: streaming results in finish order with as_completed
# ---------------------------------------------------------------------------
async def timed_task(n: int, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"result-{n} (took {delay}s)"


async def demo_as_completed() :
    print("\n=== Demo 2: as_completed (results in FINISH order) ===")
    coros = [timed_task(1, 0.3), timed_task(2, 0.1), timed_task(3, 0.2)]
    for future in asyncio.as_completed(coros):
        result = await future  # yields fastest-first: 2, 3, 1
        print(f"  ready: {result}")
        yield result


# ---------------------------------------------------------------------------
# Demo 3: per-task timeouts so one slow task fails alone
# ---------------------------------------------------------------------------
async def work_with_variable_speed(n: int, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"result-{n}"


async def guarded(coro: Awaitable[str], timeout: float, n: int) -> str:
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return f"TIMEOUT-{n} (exceeded {timeout}s)"


async def demo_per_task_timeout() -> None:
    print("\n=== Demo 3: per-task timeout (slow task fails alone) ===")
    delays = {0: 0.1, 1: 0.2, 2: 2.0, 3: 0.1}  # task 2 is too slow
    tasks = [
        guarded(work_with_variable_speed(n, d), timeout=1.0, n=n)
        for n, d in delays.items()
    ]
    for task in asyncio.as_completed(tasks):
        print(await task)
    # for r in results:
    #     print(f"  {r}")


# ---------------------------------------------------------------------------
# Demo 4: cooperative cancellation with clean-up
# ---------------------------------------------------------------------------
async def cancellable_worker() -> None:
    try:
        while True:
            await asyncio.sleep(0.4)
            print("  worker: working...")
    except asyncio.CancelledError:
        print("  worker: cleanup before stopping")
        raise  # re-raise so cancellation actually completes


async def demo_cancellation() -> None:
    print("\n=== Demo 4: cancellation with clean-up ===")
    task = asyncio.create_task(demo_per_task_timeout())
    await asyncio.sleep(1.0)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("  worker cancelled cleanly")


# ---------------------------------------------------------------------------
# Demo 5: the robust runner (semaphore + retry + timeout + isolation)
# ---------------------------------------------------------------------------
@retry(
    retry=retry_if_exception_type((TransientError, asyncio.TimeoutError)),
    wait=wait_exponential(multiplier=0.1, min=0.1, max=1.0),
    stop=stop_after_attempt(3),
    reraise=True,
)
async def attempt(n: int, timeout: float) -> str:
    """One time-bounded attempt. May raise TransientError / TimeoutError (retried)
    or PermanentError (not retried)."""
    return await asyncio.wait_for(_do_work(n), timeout=timeout)


async def _do_work(n: int) -> str:
    # Simulate realistic mixed outcomes.
    await asyncio.sleep(random.uniform(0.05, 0.25))
    roll = random.random()

    if n == 7:
        raise PermanentError(f"item {n}: invalid input (never retry)")
    if roll < 0.35:
        raise TransientError(f"item {n}: transient glitch")
    return f"value-{n}"


async def run_one(sem: asyncio.Semaphore, n: int, timeout: float) -> Dict[str, object]:
    async with sem:  # concurrency cap is the OUTERMOST layer
        try:
            value = await attempt(n, timeout)
            return {"id": n, "ok": True, "value": value}
        except Exception as exc:  # isolation: capture, never crash the batch
            return {"id": n, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


async def run_batch(
    items: List[int], concurrency: int, timeout: float
) -> List[Dict[str, object]]:
    sem = asyncio.Semaphore(concurrency)
    return await asyncio.gather(*(run_one(sem, n, timeout) for n in items))


async def demo_robust_runner() -> None:
    print("\n=== Demo 5: robust runner (semaphore + retry + timeout + isolation) ===")
    items = list(range(10))
    concurrency = 10
    timeout = 0.5

    start = time.perf_counter()
    results = await run_batch(items, concurrency=concurrency, timeout=timeout)
    elapsed = time.perf_counter() - start

    succeeded = [r for r in results if r["ok"]]
    failed = [r for r in results if not r["ok"]]

    print(f"  concurrency={concurrency}, timeout={timeout}s, elapsed={elapsed:.2f}s")
    print(f"  succeeded: {len(succeeded)}/{len(results)}")
    for r in failed:
        print(f"    FAILED item {r['id']}: {r['error']}")
    print("  note: item 7 fails permanently (no retries); others may retry transiently")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
async def main() -> None:
    # random.seed(42)  # reproducible demo output
    # await demo_isolation()
    # async for result in  demo_as_completed():
    #     print(result)
    # await demo_per_task_timeout()
    # await demo_cancellation()
    await demo_robust_runner()


if __name__ == "__main__":
    asyncio.run(main())
