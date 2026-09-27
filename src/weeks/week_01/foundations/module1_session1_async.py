"""Module 1, Session 1: Async foundations by examples.

Run:
    python src/weeks/week_01/foundations/module1_session1_async.py
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass

import httpx


@dataclass
class SimulatedEndpoint:
    name: str
    delay_s: float


@dataclass
class EndpointResult:
    name: str
    delay_s: float
    elapsed_ms: float


@dataclass
class LiveApiResult:
    url: str
    ok: bool
    status_code: int | None
    elapsed_ms: float
    error: str | None


LIVE_API_URLS = [
    "https://api.github.com",
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/todos/1",
]


SEMAPHORE_URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5",
    "https://jsonplaceholder.typicode.com/posts/6",
]

async def simple_coroutine() -> str:
    await asyncio.sleep(0.2)
    return "done"


async def fetch_simulated(endpoint: SimulatedEndpoint) -> EndpointResult:
    started = asyncio.get_running_loop().time()
    await asyncio.sleep(endpoint.delay_s)
    elapsed_ms = (asyncio.get_running_loop().time() - started) * 1000
    return EndpointResult(name=endpoint.name, delay_s=endpoint.delay_s, elapsed_ms=round(elapsed_ms, 2))


async def sequential_run(endpoints: list[SimulatedEndpoint]) -> list[EndpointResult]:
    results: list[EndpointResult] = []
    for endpoint in endpoints:
        results.append(await fetch_simulated(endpoint))
    return results


async def concurrent_run(endpoints: list[SimulatedEndpoint]) -> list[EndpointResult]:
    coroutines = [fetch_simulated(endpoint) for endpoint in endpoints]
    return await asyncio.gather(*coroutines)


async def task_run(endpoints: list[SimulatedEndpoint]) -> list[EndpointResult]:
    tasks = [asyncio.create_task(fetch_simulated(endpoint)) for endpoint in endpoints]
    results: list[EndpointResult] = []
    for task in tasks:
        results.append(await task)
    return results


async def limited_worker(endpoint: SimulatedEndpoint, semaphore: asyncio.Semaphore) -> EndpointResult:
    async with semaphore:
        return await fetch_simulated(endpoint)


async def limited_concurrent_run(endpoints: list[SimulatedEndpoint], limit: int) -> list[EndpointResult]:
    semaphore = asyncio.Semaphore(limit)
    tasks = [limited_worker(endpoint, semaphore) for endpoint in endpoints]
    return await asyncio.gather(*tasks)


def print_header(title: str) -> None:
    print("\n" + "=" * 16 + f" {title} " + "=" * 16)


def print_results(results: list[EndpointResult]) -> None:
    for result in results:
        print(f"{result.name:<12} delay={result.delay_s:.2f}s elapsed={result.elapsed_ms:.2f}ms")


def measure_sync_start() -> float:
    return time.perf_counter()


def measure_sync_elapsed(start: float) -> float:
    return round((time.perf_counter() - start) * 1000, 2)


async def fetch_live(client: httpx.AsyncClient, url: str) -> LiveApiResult:
    started = asyncio.get_running_loop().time()
    try:
        response = await client.get(url)
        elapsed_ms = (asyncio.get_running_loop().time() - started) * 1000
        return LiveApiResult(
            url=url,
            ok=response.status_code < 400,
            status_code=response.status_code,
            elapsed_ms=round(elapsed_ms, 2),
            error=None,
        )
    except Exception as err:  # Broad catch is intentional for learning diagnostics.
        elapsed_ms = (asyncio.get_running_loop().time() - started) * 1000
        return LiveApiResult(
            url=url,
            ok=False,
            status_code=None,
            elapsed_ms=round(elapsed_ms, 2),
            error=str(err),
        )


def print_live_results(results: list[LiveApiResult], label: str, elapsed_ms: float) -> None:
    print(f"{label} total elapsed: {elapsed_ms:.2f}ms")
    for item in results:
        code = item.status_code if item.status_code is not None else "-"
        state = "OK" if item.ok else "FAIL"
        print(f"[{state}] {item.url} | status={code} | elapsed={item.elapsed_ms:.2f}ms")
        if item.error:
            print(f"       error={item.error}")


async def serial_live_calls(client: httpx.AsyncClient, urls: list[str]) -> tuple[list[LiveApiResult], float]:
    started = measure_sync_start()
    results: list[LiveApiResult] = []
    for url in urls:
        results.append(await fetch_live(client, url))
    return results, measure_sync_elapsed(started)


async def parallel_live_calls(client: httpx.AsyncClient, urls: list[str]) -> tuple[list[LiveApiResult], float]:
    started = measure_sync_start()
    results = await asyncio.gather(*[fetch_live(client, url) for url in urls])
    return results, measure_sync_elapsed(started)


async def dependency_live_calls(client: httpx.AsyncClient) -> tuple[list[LiveApiResult], str]:
    first_url = "https://jsonplaceholder.typicode.com/posts/1"
    first_result = await fetch_live(client, first_url)

    if not first_result.ok:
        return [first_result], "dependency step skipped because first call failed"

    response = await client.get(first_url)
    user_id = response.json().get("userId", 1)
    second_url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    second_result = await fetch_live(client, second_url)
    return [first_result, second_result], f"dependency used userId={user_id}"


async def done_callback_calls(client: httpx.AsyncClient, urls: list[str]) -> tuple[list[LiveApiResult], list[str], float]:
    started = measure_sync_start()
    completion_order: list[str] = []

    def on_done(task: asyncio.Task[LiveApiResult]) -> None:
        try:
            completion_order.append(task.result().url)
        except Exception:
            completion_order.append("task-error")

    tasks: list[asyncio.Task[LiveApiResult]] = []
    for url in urls:
        task = asyncio.create_task(fetch_live(client, url))
        task.add_done_callback(on_done)
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results, completion_order, measure_sync_elapsed(started)


async def cancellation_calls(client: httpx.AsyncClient) -> list[LiveApiResult]:
    urls = [
        "https://httpbin.org/delay/5",
        "https://httpbin.org/delay/4",
        "https://jsonplaceholder.typicode.com/todos/1",
    ]
    tasks = [asyncio.create_task(fetch_live(client, url)) for url in urls]

    await asyncio.sleep(1.0)
    for task in tasks:
        if not task.done():
            task.cancel()

    results: list[LiveApiResult] = []
    for url, task in zip(urls, tasks):
        try:
            results.append(await task)
        except asyncio.CancelledError:
            results.append(
                LiveApiResult(
                    url=url,
                    ok=False,
                    status_code=None,
                    elapsed_ms=0.0,
                    error="cancelled",
                )
            )
    return results


async def semaphore_live_calls(client: httpx.AsyncClient, urls: list[str], limit: int) -> tuple[list[LiveApiResult], float]:
    semaphore = asyncio.Semaphore(limit)

    async def limited_fetch(url: str) -> LiveApiResult:
        async with semaphore:
            return await fetch_live(client, url)

    started = measure_sync_start()
    results = await asyncio.gather(*[limited_fetch(url) for url in urls])
    return results, measure_sync_elapsed(started)


async def main() -> None:
    random.seed(11)
    endpoints = [
        SimulatedEndpoint("users", round(random.uniform(0.2, 0.8), 2)),
        SimulatedEndpoint("orders", round(random.uniform(0.2, 0.8), 2)),
        SimulatedEndpoint("products", round(random.uniform(0.2, 0.8), 2)),
        SimulatedEndpoint("health", round(random.uniform(0.2, 0.8), 2)),
        SimulatedEndpoint("billing", round(random.uniform(0.2, 0.8), 2)),
    ]

    print_header("Example 1: coroutine and await")
    result = await simple_coroutine()
    print(f"simple_coroutine returned: {result}")

    print_header("Example 2: sequential vs concurrent (simulated)")
    start = measure_sync_start()
    seq_results = await sequential_run(endpoints)
    seq_elapsed = measure_sync_elapsed(start)
    print("Sequential results:")
    print_results(seq_results)
    print(f"Sequential total elapsed: {seq_elapsed}ms")

    start = measure_sync_start()
    con_results = await concurrent_run(endpoints)
    con_elapsed = measure_sync_elapsed(start)
    print("Concurrent results with gather:")
    print_results(con_results)
    print(f"Concurrent total elapsed: {con_elapsed}ms")

    print_header("Example 3: create_task (simulated)")
    start = measure_sync_start()
    task_results = await task_run(endpoints)
    task_elapsed = measure_sync_elapsed(start)
    print_results(task_results)
    print(f"create_task total elapsed: {task_elapsed}ms")

    print_header("Example 4: semaphore-limited concurrency (simulated)")
    start = measure_sync_start()
    limited_results = await limited_concurrent_run(endpoints, limit=3)
    limited_elapsed = measure_sync_elapsed(start)
    print_results(limited_results)
    print(f"Limited concurrency total elapsed (limit=3): {limited_elapsed}ms")

    timeout = httpx.Timeout(10.0)
    headers = {"User-Agent": "module1-session1-async-lab/1.0"}
    async with httpx.AsyncClient(timeout=timeout, headers=headers, follow_redirects=True) as client:
        print_header("Real API: serial calls")
        serial_results, serial_elapsed = await serial_live_calls(client, LIVE_API_URLS)
        print_live_results(serial_results, label="Serial", elapsed_ms=serial_elapsed)

        print_header("Real API: parallel calls")
        parallel_results, parallel_elapsed = await parallel_live_calls(client, LIVE_API_URLS)
        print_live_results(parallel_results, label="Parallel", elapsed_ms=parallel_elapsed)

        print_header("Real API: dependency chain")
        dependency_results, dependency_note = await dependency_live_calls(client)
        print_live_results(dependency_results, label="Dependency", elapsed_ms=0.0)
        print(dependency_note)

        print_header("Real API: done callbacks")
        done_results, completion_order, done_elapsed = await done_callback_calls(client, LIVE_API_URLS)
        print_live_results(done_results, label="Done callback", elapsed_ms=done_elapsed)
        print(f"Completion order: {completion_order}")

        print_header("Real API: cancellation")
        cancelled_results = await cancellation_calls(client)
        print_live_results(cancelled_results, label="Cancellation", elapsed_ms=0.0)

        print_header("Real API: semaphore-limited")
        sem_results, sem_elapsed = await semaphore_live_calls(client, SEMAPHORE_URLS, limit=2)
        print_live_results(sem_results, label="Semaphore limit=2", elapsed_ms=sem_elapsed)

    print_header("Session 1 mini project summary")
    print("You executed serial, parallel, dependency, cancellation, done callback, and semaphore patterns on public APIs.")
    print("Next exercise: change semaphore limit from 2 to 3 and compare total elapsed.")


if __name__ == "__main__":
    asyncio.run(main())
