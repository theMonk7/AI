"""Week 1 | Session 2 | File: reliable_client.py
Topic: Reliability patterns every production AI client needs.

Three core patterns taught here:
  1. Transient vs permanent errors — not all failures should be retried
  2. Exponential backoff with jitter — how tenacity handles retry spacing
  3. Timeout — never let a hanging call block forever

Real-world context:
  - OpenAI API returns 429 (rate limit) → should retry with backoff
  - OpenAI API returns 401 (bad key) → should NOT retry, fail immediately
  - Any API call can hang → must have a timeout

Run:
    python src/weeks/week_01/foundations/reliable_client.py
"""

import asyncio
import random
from dataclasses import dataclass

from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


# ─────────────────────────────────────────────
# CONCEPT: Custom exception hierarchy
# ─────────────────────────────────────────────
# Separate transient (safe to retry) from permanent (must not retry).
# This is a standard pattern in production AI clients.
class TransientAPIError(RuntimeError):
    """Temporary failure — network hiccup, rate limit, 503. Safe to retry."""

class PermanentAPIError(RuntimeError):
    """Permanent failure — bad API key, 404 not found. Must NOT retry."""


@dataclass
class APIResponse:
    ok: bool
    payload: str


# ─────────────────────────────────────────────
# CONCEPT: @retry decorator from tenacity
# ─────────────────────────────────────────────
# retry_if_exception_type(TransientAPIError)
#   → only retry if a TransientAPIError is raised
#   → PermanentAPIError will NOT be caught by retry, propagates immediately
#
# wait_exponential(multiplier=0.2, min=0.2, max=2.0)
#   → 1st retry: wait ~0.2s
#   → 2nd retry: wait ~0.4s
#   → 3rd retry: wait ~0.8s
#   → never waits more than 2.0s
#   This is called "exponential backoff" — each retry waits longer.
#   Why? Because if a service is overloaded, hammering it immediately makes it worse.
#
# stop_after_attempt(4)
#   → give up after 4 total attempts (1 original + 3 retries)
@retry(
    retry=retry_if_exception_type(TransientAPIError),
    wait=wait_exponential(multiplier=0.2, min=0.2, max=2.0),
    stop=stop_after_attempt(4),
)
async def unreliable_api_call(request_id: str) -> APIResponse:
    """Simulates a real API that fails transiently 65% of the time."""
    p = random.random()
    print(f"We run this unreliable api call {p}")
    if p < 0.65:
        # Transient: safe to retry (e.g. 503, 429, network reset)
        print("We throw error")
        raise TransientAPIError(f"Temporary failure for request={request_id}")
    await asyncio.sleep(0.1)
    return APIResponse(ok=True, payload=f"processed:{request_id}")


# ─────────────────────────────────────────────
# CONCEPT: asyncio.wait_for — timeout wrapper
# ─────────────────────────────────────────────
# wait_for(coro, timeout=N) cancels the coroutine if it hasn't
# finished within N seconds and raises asyncio.TimeoutError.
# Without this, a hanging API call can block your program forever.
async def call_with_timeout(request_id: str, timeout_s: float = 2.0) -> APIResponse:
    return await asyncio.wait_for(unreliable_api_call(request_id), timeout=timeout_s)


# ─────────────────────────────────────────────
# CONCEPT: Permanent error (no retry)
# ─────────────────────────────────────────────
async def permanent_failure_demo() -> None:
    """Shows that PermanentAPIError bypasses retry logic entirely."""
    try:
        raise PermanentAPIError("Invalid API key — fix config, do not retry")
    except PermanentAPIError as err:
        print(f"[permanent] {err} — not retried")


# ─────────────────────────────────────────────
# DEMO: run all patterns
# ─────────────────────────────────────────────
async def demo() -> None:
    # print("─── Pattern 1: retry with exponential backoff ───")
    # random.seed(7)
    # try:
    #     response = await call_with_timeout(request_id="job-001", timeout_s=5.0)
    #     print(f"[success] {response}")
    # except RetryError as err:
    #     print(f"[retry exhausted] all 4 attempts failed: {err}")
    # except asyncio.TimeoutError:
    #     print("[timeout] operation exceeded time limit")
    #
    # print()
    # print("─── Pattern 2: permanent error, no retry ───")
    # await permanent_failure_demo()
    #
    # print()
    print("─── Pattern 3: retry exhausted demo ───")
    # Force failure every time (seed that always hits p < 0.65)
    #
    # try:
    #     await call_with_timeout(request_id="job-002", timeout_s=10.0)
    # except RetryError:
    #     print("[retry exhausted] gave up after 4 attempts as expected")
    #
    # print()
    # print("─── Pattern 4: timeout fires before retries complete ───")
    random.seed(4)
    try:
        # Backoff adds up: with 0.2+0.4+0.8 = 1.4s between retries
        # A 0.5s timeout will fire before the 3rd retry
        await call_with_timeout(request_id="job-003", timeout_s=0.5)
    except asyncio.TimeoutError:
        print("[timeout] fired before retries could succeed — expected")
    except RetryError:
        print("[retry exhausted] — also expected here")


if __name__ == "__main__":
    asyncio.run(demo())
