"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  WEEK 1 CAPSTONE PROJECT: Live API Health Monitor                           ║
║  File: week01_live_api_status.py                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

─── WHAT YOU ARE BUILDING ────────────────────────────────────────────────────

A script that checks the health of multiple public APIs concurrently,
validates the results, writes a JSON report, and prints a summary table.

This project ties together EVERYTHING you learned in Sessions 1, 2, and 3.
You must use each concept listed in the requirements below.

─── HOW TO SUBMIT ────────────────────────────────────────────────────────────

1. Complete every TODO section.
2. Run the script:  python src/weeks/week_01/projects/week01_live_api_status.py
3. Confirm the output looks like this:

       Week 1 API Health Monitor
       ══════════════════════════════════════════════════
       [OK  ] 200     45.23 ms   https://api.github.com
       [OK  ] 200     31.10 ms   https://jsonplaceholder.typicode.com/posts/1
       [FAIL] None       ---    https://httpbin.org/status/503
       ──────────────────────────────────────────────────
       3/4 endpoints healthy
       Report saved: artifacts/week01/api_health_report.json

4. Show the script and the terminal output to get graded.

─── APIS TO USE (all free, no key needed) ────────────────────────────────────

  "https://api.github.com"                          → GitHub root (200, fast)
  "https://jsonplaceholder.typicode.com/posts/1"    → Fake REST API (200, fast)
  "https://jsonplaceholder.typicode.com/users/1"    → Fake user API (200, fast)
  "https://httpbin.org/get"                         → Echo service (200, slow)
  "https://httpbin.org/status/503"                  → Simulates server error (503)
  "https://httpbin.org/delay/3"                     → Simulates slow endpoint (3s)

  You MUST include at least 5 endpoints in DEFAULT_ENDPOINTS.
  At least one should be the 503 endpoint so you can see FAIL in action.

─── REQUIREMENTS AND CONCEPT MAP ─────────────────────────────────────────────

  REQ-1  [Session 1] Define DEFAULT_ENDPOINTS as a list of URL strings.

  REQ-2  [Session 1] Use a @dataclass called EndpointResult with these fields:
           url (str), ok (bool), status_code (Optional[int]),
           latency_ms (Optional[float]), error (Optional[str])

  REQ-3  [Session 3] Define a Pydantic MonitorReport model that validates
           the final JSON artifact shape. It must include:
           - generated_at_utc (str)
           - python_version (str)
           - platform (str)
           - summary: nested model with total/successful/failed (all int >= 0)
           - results: list of endpoint result schemas

  REQ-4  [Session 1] Write an async function fetch_endpoint(client, url, semaphore)
           that:
           - acquires the semaphore before making the request
           - measures latency in milliseconds using asyncio loop time
           - returns EndpointResult with status_code, latency, ok flag
           - catches ALL exceptions and returns EndpointResult with ok=False

  REQ-5  [Session 1] Write async run_monitor(endpoints) that:
           - creates an httpx.AsyncClient with a 10-second timeout
           - creates a Semaphore limiting to 3 concurrent requests
           - uses asyncio.gather() to run all fetch_endpoint calls concurrently
           - returns a list of EndpointResult

  REQ-6  [Session 3] Write write_report(results) that:
           - builds a dict payload with generated_at_utc, python_version,
             platform, summary counts, and results list
           - validates the payload using MonitorReport.model_validate()
             BEFORE writing (if shape is wrong, it must raise, not silently write)
           - writes the validated payload to artifacts/week01/api_health_report.json
           - returns the Path of the written file

  REQ-7  [Session 1] Write print_summary(results, report_path) that:
           - prints a header line
           - for each result prints: [OK  ] or [FAIL], status code,
             latency in ms, and the URL
           - for FAIL results, also prints the error message
           - prints a final count line: "X/N endpoints healthy"
           - prints the report path

  REQ-8  [Session 1] Write async main() that calls run_monitor, write_report,
           print_summary in order.

  REQ-9  [Session 1] Run main with asyncio.run(main()) — exactly once.

─── GRADING RUBRIC (25 points total) ─────────────────────────────────────────

  [5 pts]  Script runs without errors end-to-end.
  [3 pts]  REQ-4: semaphore used correctly inside fetch_endpoint.
  [3 pts]  REQ-4: latency is measured correctly around the await.
  [3 pts]  REQ-4: exceptions caught and mapped to EndpointResult(ok=False).
  [3 pts]  REQ-5: asyncio.gather used (not sequential loop).
  [4 pts]  REQ-3 + REQ-6: MonitorReport Pydantic model validates before write.
  [3 pts]  REQ-7: console output has correct [OK]/[FAIL] rows and final count.
  [1 pt]   REQ-9: asyncio.run(main()) appears exactly once.

─── HINTS ────────────────────────────────────────────────────────────────────

  Hint 1: Use asyncio.get_running_loop().time() for loop-accurate timing.
  Hint 2: Use `async with semaphore:` inside fetch_endpoint, wrapping the try block.
  Hint 3: httpx.Timeout(10.0) sets a 10-second timeout for the whole request.
  Hint 4: `response.status_code < 400` is the ok condition.
  Hint 5: In Python 3.9, use Optional[int] from typing, not int | None.
  Hint 6: asdict() from dataclasses converts EndpointResult to a plain dict.
  Hint 7: Path.mkdir(parents=True, exist_ok=True) creates nested folders safely.

─── DO NOT LOOK AT THE SOLUTION ──────────────────────────────────────────────

  The working solution is archived. You build yours from scratch using the hints
  and your session notes. Looking up syntax is fine. Copying a solution is not.

══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import asyncio
import json
import platform
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional

import httpx
from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════
# REQ-1: List of API endpoints to monitor
# ══════════════════════════════════════════════════════════════
# TODO: Fill in at least 5 endpoints from the list in the brief above.
# At least one must be the 503 endpoint.

DEFAULT_ENDPOINTS: List[str] = [
    "https://api.github.com",                          # GitHub root (200, fast)
    "https://jsonplaceholder.typicode.com/posts/1",    # Fake REST API (200, fast)
    "https://jsonplaceholder.typicode.com/users/1",    # Fake user API (200, fast)
    "https://httpbin.org/get",                         # Echo service (200, slow)
    "https://httpbin.org/status/503",                  # Simulates server error (503)
    "https://httpbin.org/delay/3",                    # Delayed response (200, slow)
]


# ══════════════════════════════════════════════════════════════
# REQ-2: Result data class
# ══════════════════════════════════════════════════════════════
# TODO: Define EndpointResult as a @dataclass.
# Fields: url (str), ok (bool), status_code (Optional[int]),
#         latency_ms (Optional[float]), error (Optional[str])
@dataclass
class EndpointResult:
    url: str
    ok: bool
    status_code: Optional[int] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════
# REQ-3: Pydantic validation model for the JSON report
# ══════════════════════════════════════════════════════════════
# TODO: Define three Pydantic models:
#   1. EndpointResultSchema  — mirrors EndpointResult fields, all Optional where needed
#   2. ReportSummary         — total, successful, failed (all int, ge=0)
#   3. MonitorReport         — generated_at_utc, python_version, platform,
#                              summary: ReportSummary, results: list[EndpointResultSchema]
class EndpointResultSchema(BaseModel):
    url: str
    ok: bool
    status_code: Optional[int] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None

class ReportSummary(BaseModel):
    total: int = Field(ge=0)
    successful: int = Field(ge=0)
    failed: int = Field(ge=0)

class MonitorReport(BaseModel):
    generated_at_utc: str
    python_version: str
    platform: str
    summary: ReportSummary
    results: List[EndpointResultSchema]

# ══════════════════════════════════════════════════════════════
# REQ-4: Single async fetch with semaphore + error capture
# ══════════════════════════════════════════════════════════════
# TODO: Implement this function.
async def fetch_endpoint(
    client: httpx.AsyncClient,
    url: str,
    semaphore: asyncio.Semaphore,
) -> EndpointResult:  # type: ignore[name-defined]
    """
    Fetch one URL with bounded concurrency.

    Steps:
      1. Acquire the semaphore (async with semaphore:)
      2. Record start time using asyncio.get_running_loop().time()
      3. await client.get(url)
      4. Calculate elapsed_ms
      5. Return EndpointResult with ok = (status_code < 400)
      6. If ANY exception occurs, catch it and return EndpointResult(ok=False, error=str(err))
    """
    # TODO: implement
    async with semaphore:
        start_time = asyncio.get_running_loop().time()
        try:
            response = await client.get(url)
            elapsed_ms = (asyncio.get_running_loop().time() - start_time) * 1000
            return EndpointResult(
                url=url,
                ok=response.status_code < 400,
                status_code=response.status_code,
                latency_ms=round(elapsed_ms, 2),
            )
        except Exception as err:
            elapsed_ms = (asyncio.get_running_loop().time() - start_time) * 1000
            return EndpointResult(
                url=url,
                ok=False,
                status_code=None,
                latency_ms=round(elapsed_ms, 2),
                error=str(err),
            )


# ══════════════════════════════════════════════════════════════
# REQ-5: Orchestrator — run all fetches concurrently
# ══════════════════════════════════════════════════════════════
# TODO: Implement this function.
async def run_monitor(endpoints: List[str]) -> List[EndpointResult]:  # type: ignore[name-defined]
    """
    Run all endpoint checks concurrently.

    Steps:
      1. Create httpx.Timeout(10.0)
      2. Create asyncio.Semaphore(3)
      3. Open httpx.AsyncClient with the timeout, follow_redirects=True,
         and User-Agent header "agentic-ai-week1-monitor/1.0"
      4. Build a list of fetch_endpoint coroutines for each URL
      5. Run all with asyncio.gather() and return the results
    """
    try:
        timeout = httpx.Timeout(10.0)
        semaphore = asyncio.Semaphore(3)
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True, headers={"User-Agent": "agentic-ai-week1-monitor/1.0"}) as client:
            tasks = [fetch_endpoint(client, url, semaphore) for url in endpoints]
            results = await asyncio.gather(*tasks)
            return results
    except Exception as e:
        print(f"Error in run_monitor: {e}")
        return []


# ══════════════════════════════════════════════════════════════
# REQ-6: Write validated JSON report artifact
# ══════════════════════════════════════════════════════════════
# TODO: Implement this function.
def write_report(results: "List[EndpointResult]") -> Path:  # type: ignore[name-defined]
    """
    Build, validate, and write the JSON artifact.

    Steps:
      1. Build a payload dict with keys:
           generated_at_utc, python_version, platform, summary (dict), results (list of dicts)
         Use datetime.now(timezone.utc).isoformat() for the timestamp.
         Use asdict(r) for each EndpointResult.
      2. Call MonitorReport.model_validate(payload)  ← this MUST happen before write
      3. Create the artifacts/week01/ directory (exist_ok=True)
      4. Write payload as formatted JSON to artifacts/week01/api_health_report.json
      5. Return the Path of the written file
    """
    # TODO: implement
    try:
        payload = {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "summary": {
                "total": len(results),
                "successful": sum(1 for r in results if r.ok),
                "failed": sum(1 for r in results if not r.ok),
            },
            "results": [asdict(r) for r in results]
        }

        # Validate the payload using MonitorReport
        MonitorReport.model_validate(payload)

        # Create the artifacts/week01/ directory
        report_dir = Path("artifacts/week01")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Write the payload to JSON file
        report_path = report_dir / "api_health_report.json"
        report_path.write_text(json.dumps(payload, indent=4), encoding="utf-8")
        return report_path
    except Exception as e:
        print(f"Error in write_report: {e}")
        raise


# ══════════════════════════════════════════════════════════════
# REQ-7: Console summary table
# ══════════════════════════════════════════════════════════════
# TODO: Implement this function.
def print_summary(results: "List[EndpointResult]", report_path: Path) -> None:  # type: ignore[name-defined]
    """
    Print a formatted table to the terminal.

    Format for each row:
      [OK  ] 200     45.23 ms   https://...
      [FAIL] None       ---    https://...
                 error: Connection refused

    End with:
      X/N endpoints healthy
      Report saved: artifacts/week01/api_health_report.json
    """
    # TODO: implement
    try:
        print("Week 1 API Health Monitor")
        print("══════════════════════════════════════════════════")
        for r in results:
            status = "[OK  ]" if r.ok else "[FAIL]"
            status_code = r.status_code if r.status_code is not None else "None"
            latency = f"{r.latency_ms:.2f} ms" if r.latency_ms is not None else "---"
            print(f"{status} {status_code:<7} {latency:<10} {r.url}")
            if not r.ok and r.error:
                print(f"         error: {r.error}")

        total = len(results)
        successful = sum(1 for r in results if r.ok)
        print("──────────────────────────────────────────────────")
        print(f"{successful}/{total} endpoints healthy")
        print(f"Report saved: {report_path}")
    except Exception as err:
        raise RuntimeError(f"Failed to print summary: {err}")


# ══════════════════════════════════════════════════════════════
# REQ-8 + REQ-9: Entry point
# ══════════════════════════════════════════════════════════════
# TODO: Write async main() that calls run_monitor → write_report → print_summary.
# Then call asyncio.run(main()) exactly once below.
async def main() -> None:
    """
    Main entry point for the script.

    Steps:
      1. Call run_monitor(DEFAULT_ENDPOINTS) to get results
      2. Call write_report(results) to save the JSON artifact
      3. Call print_summary(results, report_path) to print the console summary
    """
    run_results = await run_monitor(DEFAULT_ENDPOINTS)
    report_path = write_report(run_results)
    print_summary(run_results, report_path)

# TODO: write main() here

if __name__ == "__main__":
    asyncio.run(main())
