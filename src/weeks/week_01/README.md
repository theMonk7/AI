# Week 01 Source Map

This folder keeps all Week 1 code in one place.

## Topics implemented
1. Async Python basics (`async def`, `await`, event loop)
2. Concurrency patterns (serial, parallel, gather, create_task)
3. Concurrency control (semaphore)
4. Reliability starter (retry and timeout)
5. Structured outputs with schema validation
6. Live API mini-project and artifact generation

## Folder structure
- `foundations/`
  - `async_patterns.py`
  - `reliable_client.py`
  - `module1_session1_async.py`
- `llm_core/`
  - `structured_outputs.py`
  - `agent_echo_api.py`
- `projects/`
  - `week01_live_api_status.py`

## Run commands
```bash
python src/weeks/week_01/foundations/async_patterns.py
python src/weeks/week_01/foundations/reliable_client.py
python src/weeks/week_01/llm_core/structured_outputs.py
python src/weeks/week_01/foundations/module1_session1_async.py
python src/weeks/week_01/projects/week01_live_api_status.py
```

## Revision note
Week 1 code establishes the base execution model and real API interaction patterns that later weeks will extend with retries, evals, and orchestration.
