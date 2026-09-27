"""Week 1 | Session 2 | File: async_patterns.py
Topic: Core async primitives used across all AI engineering workflows.

This file teaches four patterns in sequence:
  1. Why async exists — sync blocking vs async non-blocking
  2. run_concurrent — semaphore-bounded task pool (used in every RAG/agent pipeline)
  3. run_sequential  — baseline comparison to understand the gain
  4. summarize        — measure and communicate results

Run:
    python src/weeks/week_01/foundations/async_patterns.py

Expected output:
    [concurrent] tasks=10 avg_delay=~0.5s elapsed=~1.2s
    [sequential] tasks=10 avg_delay=~0.5s elapsed=~5.0s

Notice: concurrent elapsed ≈ slowest single task, not the sum.
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass


# ─────────────────────────────────────────────
# DATA MODEL
# ─────────────────────────────────────────────
# A dataclass is a plain Python class with auto-generated __init__, __repr__.
# We use it to carry results in a typed, readable way instead of raw dicts.
@dataclass
class TaskResult:
    task_id: int      # which task this was
    delay_s: float    # how long the simulated I/O took
    value: int        # the computed result (task_id * 10)


# ─────────────────────────────────────────────
# CORE CONCEPT: semaphore-bounded async task
# ─────────────────────────────────────────────
# The semaphore limits how many tasks run concurrently.
# `async with semaphore` acquires one slot, does work, then releases it.
# If all slots are taken, this task suspends until one is freed — without blocking the thread.
async def simulated_io_task(task_id: int, semaphore: asyncio.Semaphore) -> TaskResult:
    async with semaphore:                              # acquire a concurrency slot
        delay = round(random.uniform(0.2, 1.0), 2)
        await asyncio.sleep(delay)                     # non-blocking wait (simulates HTTP/DB)
        return TaskResult(task_id=task_id, delay_s=delay, value=task_id * 10)


# ─────────────────────────────────────────────
# PATTERN 1: concurrent with semaphore limit
# ─────────────────────────────────────────────
# gather(*tasks) starts all coroutines and waits for all to finish.
# The semaphore limits how many actually run in parallel.
# Real use: "fetch 100 embeddings from OpenAI, max 5 at a time"
async def run_concurrent(task_count: int, concurrency: int) -> list[TaskResult]:
    semaphore = asyncio.Semaphore(concurrency)
    tasks = [simulated_io_task(i, semaphore) for i in range(task_count)]
    return await asyncio.gather(*tasks)


# ─────────────────────────────────────────────
# PATTERN 2: sequential baseline (SYNC, blocks)
# ─────────────────────────────────────────────
# This is intentionally synchronous for comparison.
# time.sleep() blocks the entire thread — nothing else can run.
# This is what all code looks like before you add async.
def run_sequential(task_count: int) -> list[TaskResult]:
    results: list[TaskResult] = []
    for i in range(task_count):
        delay = round(random.uniform(0.2, 1.0), 2)
        time.sleep(delay)                              # BLOCKS — no other work possible
        results.append(TaskResult(task_id=i, delay_s=delay, value=i * 10))
    return results


# ─────────────────────────────────────────────
# MEASUREMENT HELPER
# ─────────────────────────────────────────────
def summarize(results: list[TaskResult], elapsed_s: float, mode: str) -> None:
    avg_delay = sum(r.delay_s for r in results) / len(results)
    speedup = (avg_delay * len(results)) / elapsed_s
    print(f"[{mode}] tasks={len(results)} avg_delay={avg_delay:.2f}s elapsed={elapsed_s:.2f}s speedup={speedup:.1f}x")


# ─────────────────────────────────────────────
# MAIN: run both and compare
# ─────────────────────────────────────────────
async def main() -> None:
    random.seed(42)
    task_count = 10

    # --- concurrent run ---
    start = time.perf_counter()
    concurrent_results = await run_concurrent(task_count=task_count, concurrency=3)
    concurrent_elapsed = time.perf_counter() - start

    # --- sequential run (same seed = same delays for fair comparison) ---
    random.seed(42)
    start = time.perf_counter()
    sequential_results = run_sequential(task_count=task_count)
    sequential_elapsed = time.perf_counter() - start

    summarize(concurrent_results, concurrent_elapsed, mode="concurrent")
    summarize(sequential_results, sequential_elapsed, mode="sequential ")

    print()
    print("Key takeaway:")
    print("  concurrent elapsed ≈ max(single task delay) × ceil(tasks / concurrency)")
    print("  sequential elapsed ≈ sum of all task delays")
    print()
    print("Try this experiment: change concurrency=3 to concurrency=1")
    print("  → concurrent elapsed will equal sequential elapsed")
    print("Try: change concurrency=10 (unlimited)")
    print("  → elapsed ≈ slowest single task only")


if __name__ == "__main__":
    asyncio.run(main())
