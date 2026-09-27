"""Week 2 | Session 1 lab: Async concurrency deepening.

Run:
    python src/weeks/week_02/foundations/session1_concurrency_deepening.py

Goal:
- Compare sequential vs concurrent execution.
- Measure how semaphore limits affect throughput.
- Build intuition for safe concurrency tuning.
"""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass
from time import perf_counter


@dataclass
class SimResult:
    task_id: int
    delay_s: float
    ok: bool


async def simulated_io_task(task_id: int) -> SimResult:
    """Simulate I/O latency with occasional failures."""
    delay_s = random.uniform(0.25, 1.0)
    await asyncio.sleep(delay_s)

    # Keep failure probability low so trends are visible but realistic.
    ok = random.random() > 0.08
    return SimResult(task_id=task_id, delay_s=delay_s, ok=ok)


async def run_sequential(n_tasks: int) -> tuple[list[SimResult], float]:
    started = perf_counter()
    results: list[SimResult] = []
    for i in range(n_tasks):
        results.append(await simulated_io_task(i))
    return results, perf_counter() - started


async def run_concurrent_unbounded(n_tasks: int) -> tuple[list[SimResult], float]:
    started = perf_counter()
    tasks = [simulated_io_task(i) for i in range(n_tasks)]
    results = await asyncio.gather(*tasks)
    return list(results), perf_counter() - started


async def run_concurrent_bounded(n_tasks: int, limit: int) -> tuple[list[SimResult], float]:
    sem = asyncio.Semaphore(limit)

    async def wrapped(i: int) -> SimResult:
        async with sem:
            return await simulated_io_task(i)

    started = perf_counter()
    tasks = [wrapped(i) for i in range(n_tasks)]
    results = await asyncio.gather(*tasks)
    return list(results), perf_counter() - started


def summarize(label: str, results: list[SimResult], elapsed: float) -> None:
    ok_count = sum(1 for r in results if r.ok)
    fail_count = len(results) - ok_count
    avg_delay = sum(r.delay_s for r in results) / len(results)
    print(f"{label:<28} elapsed={elapsed:>6.2f}s | ok={ok_count:>2} fail={fail_count:>2} | avg_task_delay={avg_delay:.2f}s")


async def main() -> None:
    random.seed(42)
    n_tasks = 16

    print("Week 2 Session 1: Concurrency Deepening")
    print("=" * 72)
    print(f"Task count: {n_tasks}")
    print()

    seq_results, seq_elapsed = await run_sequential(n_tasks)
    summarize("Sequential", seq_results, seq_elapsed)

    unbounded_results, unbounded_elapsed = await run_concurrent_unbounded(n_tasks)
    summarize("Concurrent (unbounded)", unbounded_results, unbounded_elapsed)

    for limit in [1,2,3,4,5,6,7,8,9,10]:
        bounded_results, bounded_elapsed = await run_concurrent_bounded(n_tasks, limit)
        summarize(f"Concurrent (semaphore={limit})", bounded_results, bounded_elapsed)

    print()
    print("Experiment tasks for you:")
    print("1) Add semaphore=1 and explain why it approximates sequential execution.")
    print("2) Add semaphore=12 and compare speed vs failures.")
    print("3) Write your recommended limit from your own run and justify it.")


if __name__ == "__main__":
    asyncio.run(main())
