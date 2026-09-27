"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  WEEK 2 CUMULATIVE PROJECT: Concurrent Web Fetch Pipeline                    ║
║  File: week02_async_scraper_pipeline.py                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

─── WHAT YOU ARE BUILDING ────────────────────────────────────────────────────

A real, small but production-shaped tool: a concurrent "content fetcher"
pipeline. You feed it a list of URLs. A pool of async workers pulls URLs from a
queue, fetches each one (with a per-request timeout + retries on transient
errors), respects a rate limit so you never hammer a host, isolates failures so
one bad URL never sinks the batch, and writes a validated JSON report.

This ties together EVERYTHING from Weeks 1 and 2:

  Week 1:  async/await, httpx.AsyncClient, Pydantic models, dataclasses,
           gather, latency measurement, JSON artifact.
  Week 2:  bounded concurrency, timeouts, retries + backoff, failure isolation,
           asyncio.Queue, a fixed worker pool, graceful shutdown, rate limiting.

This is the kind of tool people actually build at work (crawler front-ends,
link checkers, ingestion pre-fetchers).

─── HOW TO SUBMIT ────────────────────────────────────────────────────────────

1. Complete every TODO section below.
2. Run it:  python src/weeks/week_02/projects/week02_async_scraper_pipeline.py
3. Confirm the output looks roughly like:

       Week 2 Concurrent Fetch Pipeline
       ══════════════════════════════════════════════════
       [OK  ] 200    142.5 ms   1 try    https://example.com
       [OK  ] 200     88.1 ms   2 tries  https://httpbin.org/status/200
       [FAIL] ---        ---    3 tries  https://httpbin.org/status/503
       [FAIL] ---        ---    1 try    https://httpbin.org/delay/10  (timeout)
       ──────────────────────────────────────────────────
       workers=4  rate=5/s  elapsed=3.10s
       2/4 succeeded
       Report saved: artifacts/week02/fetch_report.json

4. Show the script + terminal output + the JSON artifact to get graded.

─── URLS TO USE (all free, no key needed) ────────────────────────────────────

  "https://example.com"                       → simple 200
  "https://httpbin.org/status/200"            → 200
  "https://httpbin.org/status/503"            → always 503 (exhausts retries)
  "https://httpbin.org/delay/10"              → too slow → your timeout fires
  "https://httpbin.org/status/429"            → rate-limited response
  "https://jsonplaceholder.typicode.com/posts/1"  → 200 JSON

  Include AT LEAST 6 URLs, with at least one 503 and one /delay/10 so you can
  SEE retries exhaust and a timeout fire.

─── REQUIREMENTS AND CONCEPT MAP ─────────────────────────────────────────────

  REQ-1  [W1] Define DEFAULT_URLS: a list of at least 6 URL strings.

  REQ-2  [W1] Define custom error types:
           - TransientFetchError(RuntimeError)  → retry these
           - PermanentFetchError(RuntimeError)  → never retry these

  REQ-3  [W1] Use a @dataclass FetchResult with fields:
           url (str), ok (bool), status_code (Optional[int]),
           latency_ms (Optional[float]), attempts (int), error (Optional[str])

  REQ-4  [W1/W3] Define a Pydantic FetchReport model (+ nested summary) that
           validates the JSON artifact. Include:
           - generated_at_utc (str), workers (int>=1), rate_per_sec (float>0)
           - summary: total/succeeded/failed (all int>=0)
           - results: list of per-URL result schemas
           (Python 3.9: use Optional[...] / List[...] from typing, NOT int|None.)

  REQ-5  [W2 S3] Implement a RateLimiter class (token spacing) with an
           async acquire() guarded by an asyncio.Lock.

  REQ-6  [W1/W2 S2] Implement fetch_once(client, url) that:
           - does ONE attempt with httpx
           - maps 5xx / 429 / network errors -> TransientFetchError
           - maps 4xx (except 429) -> PermanentFetchError
           - returns (status_code, latency_ms) on success

  REQ-7  [W2 S2] Wrap fetch_once with retry (tenacity):
           - retry only TransientFetchError
           - wait_exponential, stop_after_attempt(3)
           - each attempt bounded by asyncio.wait_for(timeout=5.0)
           - count how many attempts were made

  REQ-8  [W2 S3] Implement a worker(queue, ...) coroutine that loops:
           get URL -> rate_limiter.acquire() -> fetch(with retry) ->
           append a FetchResult (isolating any exception) -> task_done()
           (task_done() MUST be in a finally block.)

  REQ-9  [W2 S3] Implement run_pipeline(urls, workers, rate) that:
           - creates an asyncio.Queue and preloads all URLs
           - starts a FIXED pool of `workers` worker tasks
           - shares ONE RateLimiter and ONE httpx.AsyncClient
           - awaits queue.join(), then cancels workers (graceful shutdown)
           - returns the list of FetchResult

  REQ-10 [W1] write_report(results, ...) that builds a validated FetchReport
           and writes it to artifacts/week02/fetch_report.json (overwrite).

  REQ-11 [W1] print_summary(results, ...) printing the table shown above plus
           the "X/Y succeeded" line and the report path.

  REQ-12 [W1] A single main() run with exactly ONE asyncio.run(main()).

─── GRADING RUBRIC (25 points) ───────────────────────────────────────────────

   5  Correctness: runs clean, exactly one asyncio.run, artifact written
   5  Concurrency: fixed worker pool + queue.join + graceful shutdown
   4  Resilience: per-attempt timeout + retry on transient only + attempts count
   4  Rate limiting: shared RateLimiter actually paces requests (elapsed ~ items/rate)
   4  Failure isolation: one bad URL never crashes the batch; failures reported
   3  Data hygiene: Pydantic validates artifact; dataclass used; 3.9 typing rules

  Bonus (+2): add a --workers / --rate CLI via argparse and show two runs
              (e.g. workers=1 vs 8) with different elapsed times.

═══════════════════════════════════════════════════════════════════════════════
  YOUR IMPLEMENTATION BELOW — fill in every TODO.
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import httpx
from pydantic import BaseModel, Field
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# ---------------------------------------------------------------------------
# REQ-1: URLs
# ---------------------------------------------------------------------------
DEFAULT_URLS: List[str] = [
    # TODO: at least 6 URLs, including one 503 and one /delay/10
    "https://example.com",#                       → simple 200
    "https://httpbin.org/status/200" ,#           → 200
    "https://httpbin.org/status/503", #            → always 503(exhaustsretries)
    "https://httpbin.org/delay/10" ,#             → too slow → your timeout fires
    "https://httpbin.org/status/429" ,#           → rate - limited response
    "https://jsonplaceholder.typicode.com/posts/1",#  → 200 JSON
]

REPORT_PATH = Path("artifacts/week02/fetch_report.json")
PER_ATTEMPT_TIMEOUT = 5.0


# ---------------------------------------------------------------------------
# REQ-2: error taxonomy
# ---------------------------------------------------------------------------
class TransientFetchError(RuntimeError):
    """Temporary failure (5xx, 429, network) — safe to retry."""


class PermanentFetchError(RuntimeError):
    """Permanent failure (most 4xx) — do not retry."""


# ---------------------------------------------------------------------------
# REQ-3: per-URL result (dataclass)
# ---------------------------------------------------------------------------
@dataclass
class FetchResult:
    url: str
    ok: bool
    status_code: Optional[int]
    latency_ms: Optional[float]
    attempts: int
    error: Optional[str]


# ---------------------------------------------------------------------------
# REQ-4: validated report schema (Pydantic)
# ---------------------------------------------------------------------------
class ResultSchema(BaseModel):
    url: str
    ok: bool
    status_code: Optional[int] = None
    latency_ms: Optional[float] = None
    attempts: int = Field(ge=0)
    error: Optional[str] = None


class SummarySchema(BaseModel):
    total: int = Field(ge=0)
    succeeded: int = Field(ge=0)
    failed: int = Field(ge=0)


class FetchReport(BaseModel):
    generated_at_utc: str
    workers: int = Field(ge=1)
    rate_per_sec: float = Field(gt=0)
    summary: SummarySchema
    results: List[ResultSchema]


# ---------------------------------------------------------------------------
# REQ-5: rate limiter (token spacing)
# ---------------------------------------------------------------------------
class RateLimiter:
    def __init__(self, rate: float) -> None:
        # TODO: store min interval (1/rate), last timestamp, and an asyncio.Lock
        self._last = 0.0
        self.__lock = asyncio.Lock()
        self._min_interval = 1.0/rate

    async def acquire(self) -> None:
        # TODO: under the lock, sleep just enough to keep <= `rate` ops/sec
        async with self.__lock:
            now = time.monotonic()
            wait = self._min_interval - (now - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last = time.monotonic()



# ---------------------------------------------------------------------------
# REQ-6: one fetch attempt
# ---------------------------------------------------------------------------
async def fetch_once(client: httpx.AsyncClient, url: str) -> "tuple[int, float]":
    """Do ONE attempt. Return (status_code, latency_ms) or raise
    Transient/Permanent error."""
    # TODO:
    #   - measure start time
    #   - try client.get(url); on httpx transport errors -> TransientFetchError
    #   - if status in (429, 500..599) -> raise TransientFetchError
    #   - if status in 400..499 (except 429) -> raise PermanentFetchError
    #   - else return (status_code, latency_ms)
    try:
        start_time = time.monotonic()
        res = await client.get(url)
        status_code = res.status_code
        latency_ms = time.monotonic() - start_time
        if status_code in (500, 600) or status_code == 429:
            raise TransientFetchError(status_code)
        elif status_code  in (400,500) and status_code != 429:
            raise PermanentFetchError(status_code)

        return (status_code, latency_ms)

    except Exception as e:
        raise e



# ---------------------------------------------------------------------------
# REQ-7: retrying + timed fetch (returns status, latency, attempts)
# ---------------------------------------------------------------------------

async def fetch_with_policy(
    client: httpx.AsyncClient, url: str
) -> "tuple[int, float, int]":
    """Retry transient failures; bound each attempt with a timeout.
    Return (status_code, latency_ms, attempts)."""
    attempts = {"n": 0}

    @retry(
        retry=retry_if_exception_type((TransientFetchError, asyncio.TimeoutError)),
        wait=wait_exponential(multiplier=0.2, min=0.2, max=2.0),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def _attempt() -> "tuple[int, float]":
        attempts["n"] += 1
        # TODO: return await asyncio.wait_for(fetch_once(client, url),
        #                                      timeout=PER_ATTEMPT_TIMEOUT)
        ...

    status, latency = await _attempt()
    return status, latency, attempts["n"]


# ---------------------------------------------------------------------------
# REQ-8: worker
# ---------------------------------------------------------------------------
async def worker(
    name: str,
    queue: asyncio.Queue,
    client: httpx.AsyncClient,
    limiter: RateLimiter,
    results: List[FetchResult],
) -> None:
    # TODO: while True: get url; try: acquire limiter; fetch_with_policy;
    #       append OK FetchResult; except -> append FAIL FetchResult (isolation);
    #       finally: queue.task_done()
    ...


# ---------------------------------------------------------------------------
# REQ-9: the pipeline
# ---------------------------------------------------------------------------
async def run_pipeline(
    urls: List[str], workers: int, rate: float
) -> List[FetchResult]:
    # TODO:
    #   - queue = asyncio.Queue(); preload urls
    #   - limiter = RateLimiter(rate)
    #   - async with httpx.AsyncClient(timeout=...) as client:
    #       - start `workers` worker tasks (create_task)
    #       - await queue.join()
    #       - cancel workers; await gather(..., return_exceptions=True)
    #   - return results
    ...


# ---------------------------------------------------------------------------
# REQ-10: write validated report
# ---------------------------------------------------------------------------
def write_report(results: List[FetchResult], workers: int, rate: float) -> Path:
    # TODO: build FetchReport (validates), write model_dump_json to REPORT_PATH
    ...


# ---------------------------------------------------------------------------
# REQ-11: summary table
# ---------------------------------------------------------------------------
def print_summary(
    results: List[FetchResult], workers: int, rate: float, elapsed: float, path: Path
) -> None:
    # TODO: print the header, one row per result, the X/Y line, and the path
    ...


# ---------------------------------------------------------------------------
# REQ-12: single entrypoint
# ---------------------------------------------------------------------------
async def main() -> None:
    workers = 4
    rate = 5.0
    start = time.perf_counter()
    results = await run_pipeline(DEFAULT_URLS, workers=workers, rate=rate)
    elapsed = time.perf_counter() - start
    path = write_report(results, workers, rate)
    print_summary(results, workers, rate, elapsed, path)


if __name__ == "__main__":
    asyncio.run(main())
