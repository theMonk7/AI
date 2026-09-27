# Week 1 Start Guide

## Objective
Complete setup once, validate baseline scripts, and run the Week 1 live API mini-project.

## Single setup source
Use only this setup document:
- `docs/setup/environment_setup.md`

## Week 1 required runs
1. `python src/weeks/week_01/foundations/async_patterns.py`
2. `python src/weeks/week_01/foundations/reliable_client.py`
3. `python src/weeks/week_01/llm_core/structured_outputs.py`
4. `python -m pytest -q`
5. `python src/weeks/week_01/projects/week01_live_api_status.py`

## Expected outcomes
- You understand reproducible environment setup and why it matters.
- You can run baseline Python modules and tests locally.
- You can hit real APIs concurrently and generate a machine-readable report artifact.

## Stretch task
Run FastAPI service and connect n8n webhook flow:
1. Start API:
   - `uvicorn src.weeks.week_01.llm_core.agent_echo_api:app --reload --port 8000`
2. Start n8n using Docker and import flow JSON from:
   - `automation/n8n/workflows/hello_webhook_to_python.json`
3. Send POST request to webhook endpoint from n8n test UI.
