from __future__ import annotations

import asyncio

from src.weeks.week_01.foundations.async_patterns import run_concurrent


def test_run_concurrent_returns_expected_count() -> None:
    results = asyncio.run(run_concurrent(task_count=5, concurrency=2))
    assert len(results) == 5
    assert results[0].task_id == 0
