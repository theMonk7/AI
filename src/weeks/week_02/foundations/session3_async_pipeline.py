"""Week 2 | Session 3 lab: Async Pipelines — Queues, Worker Pools & Rate Limiting.

Run:
    python src/weeks/week_02/foundations/session3_async_pipeline.py

Demonstrates, in order:
    1. asyncio.Queue lifecycle (put / get / task_done / join)
    2. A fixed worker pool draining a queue
    3. Backpressure with a bounded queue (maxsize)
    4. Graceful shutdown: join+cancel, and the sentinel pattern
    5. Rate limiting (token-spacing) layered on a worker pool

Python 3.9-compatible (no asyncio.TaskGroup).
"""

from __future__ import annotations

import asyncio
import time
from typing import List, Optional


# ---------------------------------------------------------------------------
# Demo 1: queue lifecycle
# ---------------------------------------------------------------------------


async def demo_queue_basics():
    queue = asyncio.Queue(maxsize=5)
    asyncio.create_task(consumer(queue))
    for i in range(10):
        await producer(queue, f"producer-{i}")
    await queue.join()
async def producer(qu, task) -> None:
    print("\n=== Demo 1: asyncio.Queue lifecycle ===")
    await qu.put(task)
    print(f"  inserted task: {task}")
    await asyncio.sleep(0.5)


async def consumer(queue):
    try:
        while True:
            item = await queue.get()
            await asyncio.sleep(0.2)
            print(f"Consumed {item}")
            queue.task_done()
    except asyncio.CancelledError:
        print("Consumer cancelled!")
        raise


# ---------------------------------------------------------------------------
# Demo 2: worker pool draining a queue
# ---------------------------------------------------------------------------
async def pool_worker(name: str, queue: asyncio.Queue, results: List[str]) -> None:
    while True:
        item = await queue.get()
        try:
            await asyncio.sleep(0.1)  # simulated I/O work
            results.append(f"{name}->{item}")
        finally:
            queue.task_done()  # ALWAYS, even if work raised


async def demo_worker_pool() -> None:
    print("\n=== Demo 2: worker pool (4 workers, 20 items) ===")
    queue: asyncio.Queue = asyncio.Queue()
    results: List[str] = []
    for i in range(20):
        queue.put_nowait(i)

    start = time.perf_counter()
    worker_count = 2
    workers = [
        asyncio.create_task(pool_worker(f"w{n}", queue, results)) for n in range(worker_count)
    ]
    await queue.join()  # wait until all 20 items are processed
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)

    elapsed = time.perf_counter() - start
    print(f"  processed {len(results)} items with {worker_count} workers in {elapsed:.2f}s")


# ---------------------------------------------------------------------------
# Demo 3: backpressure with a bounded queue
# ---------------------------------------------------------------------------
async def demo_backpressure() -> None:
    print("\n=== Demo 3: backpressure (maxsize=2, fast producer, slow consumer) ===")
    queue: asyncio.Queue = asyncio.Queue(maxsize=2)

    async def producer() -> None:
        for i in range(5):
            await queue.put(i)  # BLOCKS when the queue is full
            print(f"  produced {i} (queue size now {queue.qsize()})")

    async def consumer() -> None:
        for _ in range(5):
            item = await queue.get()
            await asyncio.sleep(0.2)  # slow
            print(f"    consumed {item}")
            queue.task_done()

    await asyncio.gather(producer(), consumer())
    print("  note: producer paused whenever the bounded queue was full")


# ---------------------------------------------------------------------------
# Demo 4: graceful shutdown via sentinel (poison pill)
# ---------------------------------------------------------------------------
SENTINEL = None


async def sentinel_worker(name: str, queue: asyncio.Queue, results: List[str]) -> None:
    while True:
        item = await queue.get()
        try:
            if item is SENTINEL:
                print(f"  {name} received stop signal, exiting")
                return
            await asyncio.sleep(0.05)
            results.append(f"{name}->{item}")
        finally:
            queue.task_done()


async def demo_graceful_shutdown() -> None:
    print("\n=== Demo 4: graceful shutdown (sentinel per worker) ===")
    queue: asyncio.Queue = asyncio.Queue()
    results: List[str] = []
    n_workers = 3

    for i in range(9):
        queue.put_nowait(i)

    workers = [
        asyncio.create_task(sentinel_worker(f"w{n}", queue, results))
        for n in range(n_workers)
    ]

    await queue.join()  # process the 9 real items first (drain)
    for _ in range(n_workers):  # one sentinel per worker
        await queue.put(SENTINEL)
    await asyncio.gather(*workers)  # workers exit cleanly on the sentinel

    print(f"  processed {len(results)} items, all {n_workers} workers stopped cleanly")


# ---------------------------------------------------------------------------
# Demo 5: rate limiting layered on a worker pool
# ---------------------------------------------------------------------------
class RateLimiter:
    """Allow at most `rate` operations per second by spacing them out."""

    def __init__(self, rate: float) -> None:
        self._min_interval = 1.0 / rate
        self._last = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:  # serialize so workers don't all fire together
            now = time.monotonic()
            wait = self._min_interval - (now - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last = time.monotonic()


async def rate_limited_worker(
    name: str, queue: asyncio.Queue, limiter: RateLimiter, timestamps: List[float]
) -> None:
    while True:
        item = await queue.get()
        try:
            await limiter.acquire()  # pace BEFORE the "call"
            timestamps.append(time.monotonic())
        finally:
            queue.task_done()


async def demo_rate_limiting() -> None:
    print("\n=== Demo 5: rate limiting (8 workers, paced to ~5 ops/sec) ===")
    queue: asyncio.Queue = asyncio.Queue()
    limiter = RateLimiter(rate=5.0)
    timestamps: List[float] = []
    n_items = 15

    for i in range(n_items):
        queue.put_nowait(i)

    start = time.perf_counter()
    workers = [
        asyncio.create_task(rate_limited_worker(f"w{n}", queue, limiter, timestamps))
        for n in range(8)  # lots of workers...
    ]
    await queue.join()
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)

    elapsed = time.perf_counter() - start
    print(f"  {n_items} ops through 8 workers took {elapsed:.2f}s")
    print(f"  expected ~= items/rate = {n_items}/5 = {n_items / 5:.1f}s")
    print("  concurrency was high, but the RATE was capped at ~5/sec")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
async def main() -> None:
    # await demo_queue_basics()
    # await demo_worker_pool()
    # await demo_backpressure()
    # await demo_graceful_shutdown()
    await demo_rate_limiting()


if __name__ == "__main__":
    asyncio.run(main())
